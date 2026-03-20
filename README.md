# 📦 Amazon Clothing Review Analysis & Recommendation

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
