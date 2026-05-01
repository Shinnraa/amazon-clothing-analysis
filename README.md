#  Amazon Clothing Review Analysis & Recommendation

## Mô tả
Phân tích reviews và xây dựng hệ thống gợi ý sản phẩm
từ bộ dữ liệu Amazon Reviews 2023 - Clothing, Shoes and Jewelry.

##  Cấu trúc thư mục

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

## Lộ trình
| Bước | Nội dung | Notebook | Trạng thái |
|------|----------|----------|------------|
| 1 | Thu thập & Hiểu dữ liệu | 01_data_collection.ipynb | ⬜ |
| 2 | Tiền xử lý | 02_preprocessing.ipynb | ⬜ |
| 3 | EDA chuyên sâu | 03_eda.ipynb | ⬜ |
| 4 | Feature Engineering | 04_feature_engineering.ipynb | ⬜ |
| 5 | Sentiment Analysis | 05_sentiment_analysis.ipynb | ⬜ |
| 6 | Recommendation System | 06_recommendation.ipynb | ⬜ |
| 7 | Đánh giá & Báo cáo | 07_evaluation.ipynb | ⬜ |

## Dataset
- **Source**: Amazon Reviews 2023
- **URL**: https://amazon-reviews-2023.github.io/
- **Category**: Clothing, Shoes and Jewelry
- **Reviews**: 22.6M | **Users**: 7.2M | **Items**: 66.0M


##  Hướng dẫn Cài đặt (Installation)

### Bước 1: Clone dự án về máy
Mở Terminal / Git Bash và chạy lệnh sau:

```bash
https://github.com/Shinnraa/amazon-clothing-analysis.git
cd amazon_clothing_project
```

### Bước 2: Thiết lập môi trường ảo (Virtual Environment)

```bash
python -m venv venv
# Kích hoạt trên Windows:
venv\Scripts\activate
# Kích hoạt trên macOS/Linux:
source venv/bin/activate
```

### Bước 3: Cài đặt thư viện phụ thuộc

```bash
pip install -r requirements.txt
```

>  **Lưu ý:** File `requirements.txt` bao gồm các thư viện cốt lõi như `torch`, `transformers`, `scikit-learn`, `pandas`, `pyarrow`, `streamlit`.

---

##  Hướng dẫn Chạy Pipeline (Huấn luyện Mô hình)

Toàn bộ quy trình từ tiền xử lý dữ liệu đến huấn luyện mô hình được thiết kế để chạy trên **Google Colab**.

1. Tải các file trong thư mục `data/raw/` lên Google Drive cá nhân.
2. Mở lần lượt các file trong thư mục `notebooks/` bằng Google Colab.
3. Chạy tuần tự các Cells. Quá trình xử lý Big Data áp dụng kỹ thuật **Chunking** và lưu định dạng **Parquet** để tránh lỗi Out-of-Memory (OOM).
4. Sau khi huấn luyện (Bước 5 & 6), tải các file trọng số `.pt` và `.pkl` lưu vào thư mục `models/` trên máy tính cục bộ.

---

*Thực hiện bởi: **[Nguyễn Min Sáng/07]***
