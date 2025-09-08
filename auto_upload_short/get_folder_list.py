import os
import re

def extract_leading_number(folder_name):
    match = re.search(r'v(\d+)', folder_name.lower())
    return int(match.group(1)) if match else float('inf')

def save_sorted_folders_by_number(root_folder, log_file_path):
    folders = [
        os.path.join(root_folder, name)
        for name in os.listdir(root_folder)
        if os.path.isdir(os.path.join(root_folder, name)) and 'đã up' not in name.lower()
    ]

    folders = sorted(folders, key=lambda x: extract_leading_number(os.path.basename(x)))

    with open(log_file_path, 'w', encoding='utf-8') as log_file:
        for folder in folders:
            log_file.write(folder + '\n')

    print(f"Đã ghi {len(folders)} thư mục vào {log_file_path}")

# --- Thay đường dẫn tại đây ---
if __name__ == '__main__':
    root_dir = r"\\nasfmc\Ổ Sever Mới\Định\Satisfy ASMR\New folder\Short Bánh xe"
    log_file = "folders.log"
    save_sorted_folders_by_number(root_dir, log_file)
