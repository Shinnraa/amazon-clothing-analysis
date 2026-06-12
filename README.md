# Amazon Clothing Recommendation System

Dự án này xây dựng một hệ thống gợi ý (Recommender System) cá nhân hóa cho tập dữ liệu thời trang Amazon (Amazon Clothing Dataset). Hệ thống được thiết kế theo mô hình hai tầng (two-stage recommender system) tiêu chuẩn công nghiệp: **Candidate Generation (Lọc ứng viên)** và **Re-ranking (Xếp hạng chi tiết)**.

---

### 1. Giai đoạn 1: Candidate Generation (Tạo ứng viên)
Nhằm lọc nhanh từ hàng triệu sản phẩm xuống còn nhóm nhỏ ứng viên tiềm năng (ví dụ: Top 200) cho mỗi người dùng:
* **SASRec (Self-Attention Sequential Recommendation)**: Mô hình dựa trên cơ chế self-attention để nắm bắt hành vi mua sắm theo chuỗi thời gian của người dùng.
* **LightGCN (Light Graph Convolutional Networks)**: Mô hình học biểu diễn (embeddings) của người dùng và sản phẩm trên đồ thị lưỡng phân tương tác (user-item bipartite graph), bỏ qua các phép biến đổi phi tuyến phức tạp để tối ưu hiệu năng.

### 2. Giai đoạn 2: Re-ranking (Tái xếp hạng)
Sử dụng các đặc trưng chi tiết (tương tác của user, mức độ phổ biến của item, giá cả, danh mục sản phẩm, v.v.) kết hợp điểm số từ Giai đoạn 1 để xếp hạng lại:
* **XGBoost / LightGBM**: Các thuật toán cây quyết định tăng cường (Gradient Boosting Trees) để phân loại và chấm điểm tương tác.
* **FinalMLP (với BPR Pairwise Loss)**: Sử dụng kiến trúc MLP song song kết hợp cơ chế Feature Gate và Bilinear Interaction. Mô hình được tối ưu trực tiếp bằng BPR Loss trên các cặp mẫu (positive/negative) và sử dụng cơ chế Residual Gating nhằm tinh chỉnh thứ hạng từ các mô hình tầng 1 mà không phá vỡ rank gốc.
* **Borda Fusion**: Kết hợp điểm số đa nguồn (từ xếp hạng gốc và dự đoán của mô hình học sâu) để đưa ra xếp hạng đồng thuận tốt nhất.

---

## Hướng dẫn Chạy Dự án

1. **Chuẩn bị Dữ liệu**: Chạy `01. xử lý dữ liệu.ipynb` để tiền xử lý tập dữ liệu thô ban đầu.
2. **Tạo Ứng viên (Stage 1)**: 
   * Huấn luyện mô hình chuỗi thời gian tại `02_sasrec.ipynb`.
   * Huấn luyện mô hình đồ thị tại `03_lightGCN.ipynb`.
3. **Hợp nhất & Trích xuất Đặc trưng**: 
   * Chạy `04_merge.ipynb` để gộp các ứng viên từ SASRec và LightGCN.
   * Chạy `05_feature_engineering.ipynb` để tạo ra các đặc trưng cho giai đoạn Re-ranking.
4. **Xếp hạng & Huấn luyện (Stage 2)**: Lựa chọn hoặc chạy song song các mô hình:
   * `06_B_Lightgbm.ipynb` (LightGBM).
   * `06_XGboost.ipynb` (GBDT).
   * `06_finalmlp-v3.ipynb` (FinalMLP với BPR Loss - Khuyên dùng).
5. **Đánh giá Chỉ số**: Chạy `08_eval.ipynb` để đo lường các thang đo offline như Recall@K, HitRate@K, Precision@K, NDCG@K trên tập Test.

---

## Chỉ số Đánh giá (Metrics)

Hệ thống được đánh giá bằng các thang đo chuẩn dành cho bài toán Ranking/Gợi ý Top-K:
* **Recall @ K**: Tỷ lệ các sản phẩm thực tế người dùng tương tác được gợi ý thành công trong Top-K.
* **Hit Rate (HR) @ K**: Tỷ lệ người dùng nhận được ít nhất một gợi ý chính xác trong Top-K.
* **NDCG @ K (Normalized Discounted Cumulative Gain)**: Đánh giá chất lượng xếp hạng (sản phẩm đúng xếp hạng càng cao thì điểm càng lớn).
* **Precision @ K**: Tỷ lệ gợi ý chính xác trên tổng số K sản phẩm được đề xuất.
