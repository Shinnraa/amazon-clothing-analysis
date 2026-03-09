import pandas as pd
import numpy as np
import sqlite3
import json
import gzip
import gc
import os
from pathlib import Path
from sklearn.model_selection import train_test_split
from tqdm import tqdm

# Project paths
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / 'data'
RAW_DIR = DATA_DIR / 'raw'
PROCESSED_DIR = DATA_DIR / 'processed'
DB_PATH = DATA_DIR / 'database.sqlite'

# Create directories
RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 60)
print("AMAZON CLOTHING - DATA SETUP (CHUNKING MODE)")
print("=" * 60)

# Check for JSON/JSONL/GZ files
json_files = list(RAW_DIR.glob('*.json')) + \
             list(RAW_DIR.glob('*.jsonl')) + \
             list(RAW_DIR.glob('*.jsonl.gz'))

data_file = json_files[0]
print(f"\n✓ Found dataset: {data_file.name}")

is_gzipped = data_file.suffix == '.gz'

CHUNK_SIZE = 50_000

def chunk_json_file(filepath, chunk_size=CHUNK_SIZE, limit=None):
    """
    Generator: đọc file JSON/JSONL theo từng lô (chunk).
    Mỗi lần yield ra một list <= chunk_size dòng.
    Không load toàn bộ file vào RAM cùng lúc.
    """
    open_func = gzip.open if is_gzipped else open
    mode = 'rt' if is_gzipped else 'r'

    buffer = []
    total_read = 0

    with open_func(filepath, mode, encoding='utf-8') as f:
        for line in f:
            # Kiểm tra giới hạn tổng dòng (nếu chọn sample)
            if limit and total_read >= limit:
                break
            try:
                buffer.append(json.loads(line))
                total_read += 1
            except json.JSONDecodeError:
                continue

            # Khi buffer đầy chunk_size → yield ra ngoài
            if len(buffer) >= chunk_size:
                yield buffer
                buffer = []   # ✅ Xóa buffer để giải phóng RAM

    # Yield phần còn lại (lô cuối < chunk_size)
    if buffer:
        yield buffer
# =============================================================
# KẾT THÚC PHẦN SỬA generator
# =============================================================

# Column mapping
column_mapping = {
    'rating': 'rating',
    'title': 'title',
    'text': 'text',
    'images': 'images',
    'product_id': 'product_id',
    'parent_asin': 'parent_asin',
    'user_id': 'user_id',
    'timestamp': 'timestamp',
    'helpful_vote': 'helpful_votes',
    'verified_purchase': 'verified_purchase',
    'review_id': 'review_id',
    'overall': 'rating',
    'reviewText': 'text',
    'summary': 'title',
    'asin': 'product_id',
    'reviewerID': 'user_id'
}

# Hàm xử lý một chunk DataFrame
def process_chunk(df, global_id_offset):
    """
    Nhận một chunk DataFrame thô, trả về chunk đã được chuẩn hóa.
    global_id_offset: số review_id bắt đầu của lô này (để review_id không trùng).
    """
    # --- Chuẩn hóa tên cột ---
    final_columns = {}
    for col in df.columns:
        final_columns[col] = column_mapping.get(col, col)
    df = df.rename(columns=final_columns)

    # --- review_id (toàn cục, không trùng giữa các lô) ---
    if 'review_id' not in df.columns:
        df['review_id'] = range(global_id_offset + 1,
                                global_id_offset + len(df) + 1)
    # Nếu file đã có review_id thì giữ nguyên (không gán lại)

    # --- Timestamp → review_date ---
    if 'timestamp' in df.columns:
        try:
            df['review_date'] = pd.to_datetime(df['timestamp'], unit='ms', errors='coerce')
            if df['review_date'].isnull().all():
                df['review_date'] = pd.to_datetime(df['timestamp'], unit='s', errors='coerce')
        except Exception:
            df['review_date'] = pd.to_datetime(df['timestamp'], errors='coerce')

    # --- Làm sạch text ---
    if 'text' in df.columns:
        df = df[df['text'].notna()]
        df = df[df['text'].str.strip() != '']
        df = df[df['text'].str.len() >= 5]

    # --- Làm sạch rating ---
    if 'rating' in df.columns:
        df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
        df = df.dropna(subset=['rating'])
        
    for col in df.columns:
        if df[col].dtype == object:
            # Kiểm tra xem có ô nào chứa list hoặc dict không
            has_complex = df[col].apply(lambda x: isinstance(x, (list, dict))).any()
            if has_complex:
                df[col] = df[col].apply(
                    lambda x: json.dumps(x, ensure_ascii=False)
                    if isinstance(x, (list, dict)) else x
                )
    return df

# ------------------------------------------------------------------
# Hỏi người dùng chọn dataset size
# ------------------------------------------------------------------
print("\n❓ Dataset size options:")
print("   1. Full dataset (chunking tự động, không giới hạn)")
print("   2. Sample 50,000 reviews đầu tiên (để test nhanh)")

while True:
    choice = input("\nYour choice (1/2): ").strip()
    if choice in ['1', '2']:
        break
    print("Please enter 1 or 2")

if choice == '1':
    limit = None
    print("\n→ Loading FULL dataset theo từng lô 50,000 dòng...")
else:
    limit = 50_000
    print("\n→ Loading 50,000 reviews đầu tiên...")


print(f"\n📖 Bắt đầu đọc & xử lý theo lô {CHUNK_SIZE:,} dòng...")

conn = sqlite3.connect(DB_PATH)

total_written   = 0   # Tổng số dòng đã ghi vào DB
chunk_index     = 0   # Số thứ tự lô hiện tại
id_offset       = 0   # Offset để tạo review_id không trùng lặp
first_chunk     = True  # Dùng để chọn if_exists='replace' hay 'append'
columns_printed = False # Chỉ in tên cột 1 lần

for chunk_data in tqdm(
    chunk_json_file(data_file, CHUNK_SIZE, limit),
    desc="Chunks",
    unit="chunk"
):
    chunk_index += 1
    print(f"\n--- Lô #{chunk_index} | Đọc được: {len(chunk_data):,} dòng ---")

    # Bước 1: Tạo DataFrame từ lô thô
    df_chunk = pd.DataFrame(chunk_data)

    # In tên cột gốc (chỉ lần đầu)
    if not columns_printed:
        print(f"   Original columns: {list(df_chunk.columns)}")
        columns_printed = True

    # Bước 2: Xử lý (chuẩn hóa cột, làm sạch, timestamp...)
    df_chunk = process_chunk(df_chunk, global_id_offset=id_offset)
    print(f"   Sau khi làm sạch: {len(df_chunk):,} dòng hợp lệ")

    # Bước 3: Ghi vào SQLite (lô đầu dùng replace để tạo bảng mới, sau dùng append)
    if_exists_mode = 'replace' if first_chunk else 'append'
    df_chunk.to_sql('reviews', conn, if_exists=if_exists_mode, index=False)
    first_chunk = False

    total_written += len(df_chunk)
    id_offset     += len(chunk_data)   # Cập nhật offset cho lô tiếp theo
    print(f"   ✓ Đã ghi vào DB. Tổng tích lũy: {total_written:,} dòng")

    # ✅ Bước 4: XÓA CHUNK KHỎI RAM
    del chunk_data, df_chunk
    gc.collect()   # Gọi garbage collector để giải phóng ngay lập tức
    print(f"   🗑️  RAM đã được giải phóng.")

# =============================================================
# KẾT THÚC VÒNG LẶP CHUNKING
# =============================================================

print(f"\n✅ Hoàn tất đọc file. Tổng {total_written:,} reviews đã vào DB.")

# ------------------------------------------------------------------
# ✅ [SỬA] Tạo Index TRƯỚC khi đọc lại để split nhanh hơn
# ------------------------------------------------------------------
print("\n⚡ Tạo index trên bảng reviews...")
cursor = conn.cursor()
cursor.execute('CREATE INDEX IF NOT EXISTS idx_rating    ON reviews(rating)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_review_id ON reviews(review_id)')

# Kiểm tra xem có cột product_id không
cols_in_db = [row[1] for row in cursor.execute("PRAGMA table_info(reviews)").fetchall()]
if 'product_id' in cols_in_db:
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_product ON reviews(product_id)')
conn.commit()

# ------------------------------------------------------------------
# ✅ [SỬA] Tạo train/val/test split
#
# Cũ:  train_test_split(df, ...)  → cần toàn bộ df trong RAM
#
# Mới: Chỉ đọc 2 cột nhẹ (review_id + rating) từ DB → split →
#      ghi bảng "splits" → KHÔNG cần load lại toàn bộ data
# ------------------------------------------------------------------
print("\n✂️  Tạo train/val/test split (chỉ đọc 2 cột nhẹ từ DB)...")

# Đọc 2 cột đủ nhỏ để vừa RAM
ids_df = pd.read_sql("SELECT review_id, rating FROM reviews", conn)
print(f"   Đã đọc {len(ids_df):,} review_id từ DB")

if 'rating' in ids_df.columns and ids_df['rating'].notna().any():
    train_ids, temp_ids = train_test_split(
        ids_df, test_size=0.3, random_state=42, stratify=ids_df['rating']
    )
    val_ids, test_ids = train_test_split(
        temp_ids, test_size=0.5, random_state=42, stratify=temp_ids['rating']
    )
else:
    train_ids, temp_ids = train_test_split(ids_df, test_size=0.3, random_state=42)
    val_ids, test_ids   = train_test_split(temp_ids, test_size=0.5, random_state=42)

# Tạo bảng splits
train_ids = train_ids[['review_id']].copy(); train_ids['split'] = 'train'
val_ids   = val_ids[['review_id']].copy();   val_ids['split']   = 'val'
test_ids  = test_ids[['review_id']].copy();  test_ids['split']  = 'test'

splits_df = pd.concat([train_ids, val_ids, test_ids], ignore_index=True)
splits_df.to_sql('splits', conn, if_exists='replace', index=False)
cursor.execute('CREATE INDEX IF NOT EXISTS idx_splits_id ON splits(review_id)')
conn.commit()

print(f"   Train: {len(train_ids):,} | Val: {len(val_ids):,} | Test: {len(test_ids):,}")

# Giải phóng RAM
del ids_df, train_ids, val_ids, test_ids, splits_df
gc.collect()

# ------------------------------------------------------------------
# ✅ [SỬA] Xuất CSV theo từng split - đọc từ DB theo lô nhỏ
#          (tránh load toàn bộ split vào RAM)
#
# Cũ:  train_df.to_csv(...)  → cần toàn bộ train_df trong RAM
#
# Mới: Dùng chunked SQL read → ghi CSV dần (header chỉ ở lô đầu)
# ------------------------------------------------------------------
print("\n📄 Xuất CSV từ DB theo lô (chunk)...")
CSV_READ_CHUNK = 50_000   # Kích thước lô khi đọc từ DB để xuất CSV

for split_name in ['train', 'val', 'test']:
    csv_path = PROCESSED_DIR / f'{split_name}.csv'
    first_write = True

    # JOIN reviews với splits để lấy đúng tập
    query = f"""
        SELECT r.*
        FROM reviews r
        JOIN splits s ON r.review_id = s.review_id
        WHERE s.split = '{split_name}'
    """
    # Đọc từng lô từ DB
    for chunk_df in pd.read_sql(query, conn, chunksize=CSV_READ_CHUNK):
        chunk_df.to_csv(
            csv_path,
            mode='w' if first_write else 'a',   # Ghi mới hoặc append
            header=first_write,                  # Header chỉ ở lô đầu
            index=False
        )
        first_write = False
        del chunk_df
        gc.collect()

    print(f"   ✓ {split_name}.csv đã lưu → {csv_path}")

conn.close()

# ------------------------------------------------------------------
# HOÀN TẤT
# ------------------------------------------------------------------
print("\n" + "=" * 60)
print("SETUP COMPLETE! 🎉")
print(f"📁 Database : {DB_PATH}")
print(f"📁 CSV files: {PROCESSED_DIR}")
print(f"📊 Tổng reviews: {total_written:,}")
print("=" * 60)