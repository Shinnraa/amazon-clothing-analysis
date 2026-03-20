"""
⚙️ CONFIG - Cấu hình đường dẫn toàn dự án
Import file này ở đầu mỗi notebook thay vì hard-code paths
"""
import os

# Root directory (tự động detect)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Data paths
RAW_DIR       = os.path.join(ROOT_DIR, "data", "raw")
PROCESSED_DIR = os.path.join(ROOT_DIR, "data", "processed")
SAMPLE_DIR    = os.path.join(ROOT_DIR, "data", "sample")

# File paths - Raw
REVIEW_RAW  = os.path.join(RAW_DIR, "review_clothing.jsonl.gz")
META_RAW    = os.path.join(RAW_DIR, "meta_clothing.jsonl.gz")

# File paths - Processed
REVIEW_CLEAN  = os.path.join(PROCESSED_DIR, "review_clean.parquet")
META_CLEAN    = os.path.join(PROCESSED_DIR, "meta_clean.parquet")
MERGED_CLEAN  = os.path.join(PROCESSED_DIR, "merged_clean.parquet")

# File paths - Sample
REVIEW_SAMPLE = os.path.join(SAMPLE_DIR, "review_sample.parquet")
META_SAMPLE   = os.path.join(SAMPLE_DIR, "meta_sample.parquet")

# Output paths
FIGURES_DIR = os.path.join(ROOT_DIR, "outputs", "figures")
MODELS_DIR  = os.path.join(ROOT_DIR, "outputs", "models")
REPORTS_DIR = os.path.join(ROOT_DIR, "outputs", "reports")

# ============================
# SAMPLING CONFIG
# ============================
SAMPLE_RATE   = 0.05   # Lấy 5% reviews (~1.1M)
MAX_META_ROWS = 500_000  # Lấy 500k sản phẩm
MIN_TEXT_LEN  = 10       # Review tối thiểu 10 ký tự
MIN_REVIEWS_PER_USER = 5  # Lọc user có ít nhất 5 reviews (cho recommendation)
MIN_REVIEWS_PER_ITEM = 5  # Lọc item có ít nhất 5 reviews

# ============================
# MODEL CONFIG  
# ============================
RANDOM_STATE = 42
TEST_SIZE    = 0.2
