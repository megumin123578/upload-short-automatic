import os
import shutil

FOLDERS_LOG = 'folders.log'
PROGRESS_FILE = 'progress.txt'
VIDEOS_PER_BATCH = 3
MAX_VIDEOS_PER_FOLDER = 15
VIDEO_EXTS = ['.mp4', '.mov', '.avi', '.mkv']
DA_UP_FOLDER_NAME = '1. ĐÃ UP'  # Tên thư mục chứa các thư mục đã up

def get_video_files(folder):
    files = [
        f for f in os.listdir(folder)
        if os.path.isfile(os.path.join(folder, f)) and os.path.splitext(f)[1].lower() in VIDEO_EXTS
    ]
    return sorted(files)

def load_folders():
    with open(FOLDERS_LOG, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def load_progress():
    if not os.path.exists(PROGRESS_FILE):
        return 0, 0
    with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
        parts = f.read().strip().split(',')
        return int(parts[0]), int(parts[1])  # folder_index, video_index

def save_progress(folder_index, video_index):
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        f.write(f'{folder_index},{video_index}')

def move_folder_to_da_up(current_folder):
    parent_dir = os.path.dirname(current_folder)
    da_up_path = os.path.join(parent_dir, DA_UP_FOLDER_NAME)

    os.makedirs(da_up_path, exist_ok=True)
    destination = os.path.join(da_up_path, os.path.basename(current_folder))

    if not os.path.exists(destination):
        shutil.move(current_folder, destination)
        print(f"Đã di chuyển thư mục: {current_folder} → {destination}")
    else:
        print(f"Thư mục đích đã tồn tại: {destination} — không di chuyển.")

def get_next_videos():
    folders = load_folders()
    folder_index, video_index = load_progress()

    while folder_index < len(folders):
        folder = folders[folder_index]
        videos = get_video_files(folder)

        if video_index >= len(videos) or video_index >= MAX_VIDEOS_PER_FOLDER:
            # Đã lấy đủ video, move folder vào "ĐÃ UP"
            move_folder_to_da_up(folder)
            folder_index += 1
            video_index = 0
            continue

        next_videos = videos[video_index : video_index + VIDEOS_PER_BATCH]
        video_index += len(next_videos)

        save_progress(folder_index, video_index)
        return [os.path.join(folder, v) for v in next_videos]

    return []  # Hết tất cả video

if __name__ == '__main__':
    videos = get_next_videos()
    if videos:
        print("Video batch:")
        for v in videos:
            print(v)
    else:
        print("Đã xử lý hết tất cả video và thư mục.")
