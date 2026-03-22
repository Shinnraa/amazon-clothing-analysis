import os
from pathlib import Path

def create_gitkeep(root_path):
    folders_to_keep = [
        'data/raw',
        'data/processed',
        'data/sample',
        'outputs/figures',
        'notebooks',
        'src'
    ]
    
    for folder in folders_to_keep:
        dir_path = Path(root_path) / folder
        # Tạo thư mục nếu chưa có
        dir_path.mkdir(parents=True, exist_ok=True)
        # Tạo file .gitkeep
        keep_file = dir_path / ".gitkeep"
        if not keep_file.exists():
            with open(keep_file, 'w') as f:
                pass
            print(f"✅ Đã tạo .gitkeep trong: {folder}")
        else:
            print(f"ℹ️ Đã có .gitkeep trong: {folder}")

# Chạy lệnh (đảm bảo bạn đang ở thư mục gốc dự án)
create_gitkeep(os.getcwd())