"""
🗂️ AMAZON CLOTHING PROJECT - Auto Setup
Chạy file này 1 lần để tạo toàn bộ cấu trúc thư mục
"""

import os

# ============================
# CẤU TRÚC THƯ MỤC
# ============================
PROJECT_NAME = "amazon_clothing_project"

folders = [
    "data/raw",           # File gốc .jsonl.gz
    "data/processed",     # File đã xử lý .parquet
    "data/sample",        # File mẫu nhỏ để test
    "notebooks",          # Jupyter Notebooks
    "src",                # Python modules tái sử dụng
    "outputs/figures",    # Biểu đồ
    "outputs/models",     # Model đã train
    "outputs/reports",    # Báo cáo
    "docs",               # Tài liệu
]

for folder in folders:
    path = os.path.join(PROJECT_NAME, folder)
    os.makedirs(path, exist_ok=True)
    print(f"  ✅ Created: {path}")

# ============================
# TẠO FILE .gitkeep (giữ folder rỗng)
# ============================
keep_folders = ["data/raw", "data/processed", "data/sample",
                "outputs/figures", "outputs/models", "outputs/reports"]
for folder in keep_folders:
    path = os.path.join(PROJECT_NAME, folder, ".gitkeep")
    open(path, "w").close()

# ============================
# TẠO README.md
# ============================
readme = """# 📦 Amazon Clothing Review Analysis & Recommendation

## Mô tả
Phân tích reviews và xây dựng hệ thống gợi ý sản phẩm
từ bộ dữ liệu Amazon Reviews 2023 - Clothing, Shoes and Jewelry.

## 📁 Cấu trúc thư mục

```
amazon_clothing_project/
│
├── data/
│   ├── raw/                    # ← Đặt file .jsonl.gz tải về vào đây
│   │   ├── review_clothing.jsonl.gz
│   │   └── meta_clothing.jsonl.gz
│   ├── processed/              # File đã xử lý (tự động tạo)
│   │   ├── review_clean.parquet
│   │   ├── meta_clean.parquet
│   │   └── merged_clean.parquet
│   └── sample/                 # File mẫu nhỏ để test nhanh
│       ├── review_sample.parquet
│       └── meta_sample.parquet
│
├── notebooks/                  # Jupyter Notebooks
│   ├── 01_data_collection.ipynb
│   ├── 02_preprocessing.ipynb
│   ├── 03_eda.ipynb
│   ├── 04_feature_engineering.ipynb
│   ├── 05_sentiment_analysis.ipynb
│   ├── 06_recommendation.ipynb
│   └── 07_evaluation.ipynb
│
├── src/                        # Code Python module hóa
│   ├── __init__.py
│   ├── loader.py               # Hàm load dữ liệu
│   ├── preprocess.py           # Hàm tiền xử lý
│   ├── eda.py                  # Hàm visualize
│   ├── features.py             # Feature engineering
│   ├── sentiment.py            # Sentiment model
│   └── recommender.py          # Recommendation model
│
├── outputs/
│   ├── figures/                # Biểu đồ xuất ra
│   ├── models/                 # Model đã train (.pkl)
│   └── reports/                # Báo cáo kết quả
│
├── docs/                       # Tài liệu, ghi chú
├── requirements.txt            # Thư viện cần cài
├── config.py                   # Cấu hình đường dẫn
└── README.md
```

## 🗺️ Lộ trình
| Bước | Nội dung | Notebook | Trạng thái |
|------|----------|----------|------------|
| 1 | Thu thập & Hiểu dữ liệu | 01_data_collection.ipynb | ⬜ |
| 2 | Tiền xử lý | 02_preprocessing.ipynb | ⬜ |
| 3 | EDA chuyên sâu | 03_eda.ipynb | ⬜ |
| 4 | Feature Engineering | 04_feature_engineering.ipynb | ⬜ |
| 5 | Sentiment Analysis | 05_sentiment_analysis.ipynb | ⬜ |
| 6 | Recommendation System | 06_recommendation.ipynb | ⬜ |
| 7 | Đánh giá & Báo cáo | 07_evaluation.ipynb | ⬜ |

## 📊 Dataset
- **Source**: Amazon Reviews 2023
- **URL**: https://amazon-reviews-2023.github.io/
- **Category**: Clothing, Shoes and Jewelry
- **Reviews**: 22.6M | **Users**: 7.2M | **Items**: 66.0M
"""

with open(os.path.join(PROJECT_NAME, "README.md"), "w", encoding="utf-8") as f:
    f.write(readme)
print("  ✅ Created: README.md")

# ============================
# TẠO config.py
# ============================
config = '''"""
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
'''

with open(os.path.join(PROJECT_NAME, "config.py"), "w", encoding="utf-8") as f:
    f.write(config)
print("  ✅ Created: config.py")

# ============================
# TẠO requirements.txt
# ============================
requirements = """# Core
pandas>=2.0.0
numpy>=1.24.0
pyarrow>=12.0.0
fastparquet>=2023.0.0

# Visualization
matplotlib>=3.7.0
seaborn>=0.12.0
wordcloud>=1.9.0
plotly>=5.15.0

# NLP
nltk>=3.8.0
scikit-learn>=1.3.0

# Deep Learning (Bước 5 - Sentiment)
# transformers>=4.30.0
# torch>=2.0.0

# Recommendation (Bước 6)
# surprise>=1.1.3
# implicit>=0.7.0

# Utils
tqdm>=4.65.0
jupyter>=1.0.0
ipykernel>=6.0.0
"""

with open(os.path.join(PROJECT_NAME, "requirements.txt"), "w", encoding="utf-8") as f:
    f.write(requirements)
print("  ✅ Created: requirements.txt")

# ============================
# TẠO src/__init__.py
# ============================
open(os.path.join(PROJECT_NAME, "src", "__init__.py"), "w").close()
print("  ✅ Created: src/__init__.py")

# ============================
# TỔNG KẾT
# ============================
print("\n" + "="*50)
print("🎉 PROJECT SETUP HOÀN TẤT!")
print("="*50)
print(f"\n📁 Thư mục dự án: ./{PROJECT_NAME}/")
print("\n📌 Bước tiếp theo:")
print("  1. Tải data từ: https://amazon-reviews-2023.github.io/")
print("  2. Đặt file vào: data/raw/")
print("  3. Mở notebooks/01_data_collection.ipynb để bắt đầu!")
print("\n💡 Cài thư viện:")
print(f"  pip install -r {PROJECT_NAME}/requirements.txt")