import os, csv, sys, time, uuid, traceback


from datetime import datetime, timedelta, timezone
from typing import List, Dict, Optional

VIDEO_EXTS = ['.mp4', '.mov', '.avi', '.mkv']
TZ_OFFSET_HOURS = 7  # Asia/Bangkok (UTC+7)
USE_MOVE_TO_DONE = False  # move file after upload (tracking with CSV + sidecar) 


def local_now() -> datetime:
    utc_now = datetime.now(timezone.utc)
    return utc_now + timedelta(hours=TZ_OFFSET_HOURS) # return <class 'datetime.datetime'> : 2025-09-08 09:57:29.770732+00:00


def ensure_file(path: str, header: List[str]):
    if not os.path.exists(path):
        with open(path, 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f)
            w.writerow(header) #ensure csv file exist


def read_csv_dicts(path: str) -> List[Dict[str, str]]: #read csv as Dict
    if not os.path.exists(path):
        return []
    with open(path, 'r', newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f)) 
 

def write_csv_dicts(path: str, rows: List[Dict[str, str]], header: List[str]):
    tmp = path + ".tmp"
    with open(tmp, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=header)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    os.replace(tmp, path)


def append_csv_dict(path: str, row: Dict[str, str], header: List[str]):
    existed = os.path.exists(path)
    with open(path, 'a', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=header)
        if not existed:
            w.writeheader()
        w.writerow(row)


def _file_signature(path: str, quick: bool = True) -> str:
    """quick=True: dùng size+mtime; quick=False: thêm md5(1MB đầu/cuối)."""
    try:
        st = os.stat(path)
        base = f"{st.st_size}:{int(st.st_mtime)}"
        if quick:
            return base
        import hashlib
        h = hashlib.md5()
        with open(path, 'rb') as f:
            head = f.read(1024*1024)
            f.seek(max(0, st.st_size - 1024*1024))
            tail = f.read(1024*1024)
        h.update(head); h.update(tail)
        return base + ':' + h.hexdigest()
    except Exception:
        return str(uuid.uuid4())


def list_videos(root: str, max_per_folder: int) -> List[str]:
    results: List[str] = []
    if not os.path.isdir(root):
        return results
    for cur, dirs, files in os.walk(root):
        count_in_folder = 0
        for name in sorted(files):
            if count_in_folder >= max_per_folder:
                break
            ext = os.path.splitext(name)[1].lower()
            if ext in VIDEO_EXTS:
                results.append(os.path.join(cur, name))
                count_in_folder += 1
    return results


def file_signature(path: str) -> str:
    return _file_signature(path, quick=True)


def create_sidecar(video_path: str, data: Dict[str, str]):
    """Ghi file .uploaded.json cạnh video để ghi nhận trạng thái mà không di chuyển file."""
    try:
        base = os.path.splitext(video_path)[0] + '.uploaded.json'
        import json
        with open(base, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        log(f"sidecar error: {e}")



def log(msg: str):
    ts = local_now().strftime('%d-%m-%Y %H:%M:%S')
    line = f"[{ts}] {msg}"
    print(line)
    with open('uploader.log', 'a', encoding='utf-8') as f:
        f.write(line + "\n")



import shutil
import os
import random
import os
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from pathlib import Path
import time
import pyautogui
import random
import pyperclip
import webbrowser
from bs4 import BeautifulSoup
import math
import subprocess
import time
import re
from datetime import datetime, timedelta



def create_video(first_time):
    
    if first_time == 0:
        create_x, create_y = random.uniform(1686,1766), random.uniform(148,173)
        select_x, select_y = random.uniform(1687,1838), random.uniform(192,220)
    
    else:
        create_x, create_y = random.uniform(1759,1839), random.uniform(148,173)
        select_x, select_y = random.uniform(1679,1834), random.uniform(200,220)

    #go to create button    
    print(f"Move to ({create_x}, {create_y})")
    pyautogui.moveTo(create_x, create_y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad) 
    random_delay() 
    pyautogui.click()

    #select upload
    print(f"Move to ({select_x}, {select_y})")
    pyautogui.moveTo(select_x, select_y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad) 
    random_delay() 
    pyautogui.click()



    x,y = random.uniform(900,1000), random.uniform(460,549)
    print(f"Move to ({x}, {y})")
    pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad) 
    random_delay(2,3) 
    pyautogui.click()

def get_date():
    today = datetime.today()
    tomorrow = today + timedelta(days=1)
    return today.strftime("%b %d, %Y"), tomorrow.strftime("%b %d, %Y")

def increase_hash_number(text):
    # Tìm số sau dấu #
    match = re.search(r'#(\d+)', text)
    if match:
        old_number = int(match.group(1))
        new_number = old_number + 1
        # Thay thế số cũ bằng số mới
        return re.sub(r'#\d+', f'#{new_number}', text)
    else:
        # Nếu không có dấu #
        return text

def ad_suitability():
    x, y =1428, 399
    pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad)
    pyautogui.mouseDown()
    pyautogui.moveTo(x, y+800, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad) 
    pyautogui.mouseUp()
    time.sleep(random.uniform(1,2))

    location = pyautogui.locateOnScreen("img_data/confirm_content.png", confidence=0.7)
    if location:
        x, y = pyautogui.center(location) 
        pyautogui.moveTo(x,y)
        pyautogui.click()
    random_delay()

    #send submit
    location = pyautogui.locateOnScreen("img_data/send_submit.png", confidence=0.8)
    if location:
        x, y = pyautogui.center(location) 
        pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad)
        random_delay()
        pyautogui.click()
    random_delay()

    time.sleep(random.uniform(3,3.5))

    x,y = 1386,955
    print(f'Move to {x,y}')
    pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad)
    random_delay()
    pyautogui.click()
    random_mouse()


def get_video_files(folder):
    files = [
        f for f in os.listdir(folder)
        if os.path.isfile(os.path.join(folder,f)) and os.path.splitext(f)[1].lower() in ['.mp4', '.mov', '.avi', '.mkv']
    ]
    return sorted(files)

def load_folder(log_file = 'folders.log'):
    with open(log_file, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def load_progress(progress_file = 'progress.txt'):
    if not os.path.exists(progress_file):
        return 0,0
    with open(progress_file, 'r', encoding='utf8') as f:
        parts = f.read().strip().split(',')
        return int(parts[0]), int(parts[1])
    
def save_progress(folder_idx, video_idx, progress_file):
    with open(progress_file, 'w', encoding='utf-8') as f:
        f.write(f'{folder_idx},{video_idx}')

    


def move_folder(current_folder,uploaded_folder_name):
    parent_dir = os.path.dirname(current_folder)
    uploaded_path = os.path.join(parent_dir, uploaded_folder_name)

    os.makedirs(uploaded_path, exist_ok = True)
    destination = os.path.join(uploaded_path, os.path.basename(current_folder))

    if not os.path.exists(destination):
        shutil.move(current_folder, destination)
        print(f'Moved folder {current_folder} --> {destination}')
    else:
        print(f'Folder {destination} has already exists')


def get_next_video(max_videos_per_folder, uploaded_folder_name, video_per_batch):
    folders = load_folder()
    folder_idx, video_idx = load_progress()
    while folder_idx < len(folders):
        folder = folders[folder_idx]
        videos = get_video_files(folder)

        if video_idx >= len(videos) or video_idx >= max_videos_per_folder:
            # move_folder(folder, uploaded_folder_name)
            folder_idx += 1
            video_idx = 0
            continue

        next_video =videos[video_idx : video_idx + video_per_batch] 
        video_idx += len(next_video)

        save_progress(folder_idx, video_idx, 'progress.txt')
        return [os.path.join(folder, v) for v in next_video]
    
    return []





def update_name(ls):

    pass

def upload_yt():
    pass



def random_delay(min_sec = 0.5, max_sec = 1):
    time.sleep(random.uniform(min_sec, max_sec))



def off_set_(x, y, delta=5):
    rand_x = x + random.randint(-delta, delta)
    rand_y = y + random.randint(-delta, delta)
    pyautogui.moveTo(rand_x, rand_y, duration=random.uniform(0.2, 0.5))
    pyautogui.click()


def convert_date(input_date):
    date_splited = input_date.split('/')

    pl_date = f'{date_splited[0]} thg {date_splited[1]}, 20{date_splited[2]}'

    return pl_date



def access_yt_channel(url, chrome_profile_path = "Profile 11"):
    print(f"Mở trình duyệt và truy cập: {url}")
    
    chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
    profile_arg = f"--profile-directory={chrome_profile_path}"
    
    subprocess.run([chrome_path, profile_arg, url])
    
    time.sleep(4.5)


def split_dir(dir):
    #split_dir folder and filename
    folder = os.path.dirname(dir)
    filename = os.path.basename(dir)

    return folder, filename


def choose_file(folder_dir, file_name):

        x, y= 1651,49
        print(f'Move to {x,y}')
        pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad) 
        random_delay()
        pyautogui.click()
        
        #enter folder
        pyperclip.copy(folder_dir)
        pyautogui.hotkey("ctrl", "v")
        random_delay()
        pyautogui.hotkey("enter")

        x, y= 1885,47
        print(f'Move to {x,y}')
        pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad) 
        random_delay()
        pyautogui.click()
        random_delay()

        random_delay()
        #enter filename
        pyperclip.copy(file_name)
        pyautogui.hotkey("ctrl", "v")
        pyautogui.hotkey("enter")
        random_delay(2,3)

        #select file
        select_x, select_y = 232,118
        print(f'Move to {select_x, select_y}')
        pyautogui.moveTo(select_x, select_y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad)  
        random_delay()
        pyautogui.click()
        random_delay()

        pyautogui.hotkey('enter')
        time.sleep(5)
        ##########################################################################
    

def get_tag_name(html):
    soup = BeautifulSoup(html, 'html.parser')
    tag = soup.find('yt-formatted-string')
    if tag:
        return tag.text.strip()
    return None

def select_channel(channel_tag, total_channel):
    #go to def tool

    time.sleep(2)
    first_channel = [453,295]
    x,y = first_channel[0], first_channel[1]
    

    for _ in range(total_channel):

        x += 300 #move x to seccond col
        pyautogui.hotkey('ctrl','shift','c')
        time.sleep(1)
        random_delay(1,2 )
        print(f"Move to ({x}, {y})")
        pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad)  
        pyautogui.click()
        random_delay() 
        pyautogui.hotkey('ctrl','c')
        time.sleep(1)
        tag_name = get_tag_name(pyperclip.paste())
        print(tag_name)
        if tag_name == channel_tag:
            return x +275,y
        
        x += 300 #move x to third col
        pyautogui.hotkey('ctrl','shift','c')
        random_delay(1,2) 
        print(f"Move to ({x}, {y})")
        pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad)  
        pyautogui.click()
        random_delay() 
        pyautogui.hotkey('ctrl','c')
        time.sleep(1)
        tag_name = get_tag_name(pyperclip.paste())
        print(tag_name)
        if tag_name == channel_tag:
            return x+275,y

        x -= 600 #move x to first col
        y+= 63  #move y to next row
        pyautogui.hotkey('ctrl','shift','c')
        random_delay(1,2) 
        print(f"Move to ({x}, {y})")
        pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad)  
        pyautogui.click()
        random_delay() 
        pyautogui.hotkey('ctrl','c')
        time.sleep(1)
        tag_name = get_tag_name(pyperclip.paste())
        print(tag_name)
        if tag_name == channel_tag:
            return x+275,y
        

def random_mouse(so_vong=None, ban_kinh=None, toc_do=0.01, huong=None, huong_xoan='vao'):

    so_vong = int(random.uniform(1, 6)) if so_vong is None else int(so_vong)
    ban_kinh = random.uniform(100, 800) if ban_kinh is None else ban_kinh
    huong = random.choice(['thuan', 'nguoc']) if huong is None else huong

    
    tam_x, tam_y = pyautogui.position()
    pyautogui.FAILSAFE = False  # Di chuyển chuột vào góc trên bên trái để dừng
    
    
    toc_do_min = 0.0001  
    so_buoc = so_vong * 360 // 5  
    buoc_toc_do = (toc_do - toc_do_min) / so_buoc if so_buoc > 0 else 0
    
    
    buoc_r = ban_kinh / so_buoc 
    r_hien_tai = ban_kinh

    
    for _ in range(so_vong):
        for goc in range(0, 360, 5):
            pyautogui.PAUSE = toc_do
            toc_do = max(toc_do - buoc_toc_do, toc_do_min)
            
            rad = math.radians(goc if huong == 'thuan' else -goc)
            # Tính tọa độ mới
            x = tam_x + r_hien_tai * math.cos(rad)
            y = tam_y + r_hien_tai * math.sin(rad)
            pyautogui.moveTo(x, y)

            r_hien_tai += -buoc_r if huong_xoan == 'vao' else buoc_r

        r_hien_tai = max(r_hien_tai, 0)

    pyautogui.moveTo(random.uniform(500,999), random.uniform(500,999),duration=random.uniform(0.3,0.5), tween=pyautogui.easeInOutQuad)
