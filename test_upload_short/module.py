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

def excel_to_sheet(excel_file, sheet_file, worksheet_index):
    df = pd.read_excel(excel_file, engine="openpyxl")

    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    CREDS_FILE = "sheet.json"

    creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
    gc = gspread.authorize(creds)

    spreadsheet = gc.open(sheet_file)

    try:
        worksheet = spreadsheet.get_worksheet(worksheet_index)  # Lấy theo index
    except Exception as e:
        print(f"Không thể lấy worksheet tại index {worksheet_index}: {e}")
        return

    worksheet.clear()

    data = [df.columns.tolist()] + df.fillna('').astype(str).values.tolist()
    worksheet.update("A1", data)

    print(f"Đã ghi nội dung vào worksheet index {worksheet_index} trong '{sheet_file}'.")


def get_thumbnail_dir(folder_path):
    if not os.path.exists(folder_path):
        print(f"Thư mục {folder_path} không tồn tại!")
        return None

    image_extensions = ('.png', '.jpg', '.jpeg')

    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(image_extensions)]

    if len(image_files) == 1:
        return image_files[0]  
    else:
        print(f"Thư mục không chứa file ảnh (.png, .jpg, .jpeg).")
        return None
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

def clear_excel_file(excel_file):
    try:
        columns = ['first vids', 'desired length', 'output directory', 'number_of_vids', 'status']
        empty_df = pd.DataFrame(columns=columns)
        empty_df.to_excel(excel_file, index=False, engine='openpyxl')
        print(f"Cleared existing content in Excel file: {excel_file}")
    except Exception as e:
        print(f"Error clearing Excel file '{excel_file}': {e}")





def pre_process_data(file):
    df = pd.read_excel(file)
    df.columns = df.columns.str.strip()  # bỏ khoảng trắng 2 đầu
    df.columns = df.columns.str.replace('\u200b', '', regex=True)  # nếu có ký tự ẩn
    required = [
        'Channel','Title','Description','output directory','Thumbnail',
        'Publish hour','Publish date'
    ]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in Excel: {missing}. "
                        f"Check header spelling/casing/whitespace.")
    filtered_df = df[
        df['Channel'].notna() &
        df['output directory'].notna() &
        df['status'].str.lower().eq('upload')
    ]
    return filtered_df, df
def copy_from_ggsheet_to_excel(gspread_client, sheet_name, excel_file, idx):
    try:
        spreadsheet = gspread_client.open(sheet_name)
        worksheet = spreadsheet.get_worksheet(idx)
        data = worksheet.get_all_values()

        if not data:
            print("Google Sheet is empty!")
            return
        
        columns = data[0]  
        values = data[1:]  
        df = pd.DataFrame(values, columns=columns)
        clear_excel_file(excel_file)
        df.to_excel(excel_file, index=False, engine='openpyxl')
        print(f"Successfully copied data from Google {sheet_name} to Excel file {excel_file}")
    except Exception as e:
        print(f"Error copying data from Google Sheet to Excel: {e}")

import subprocess
import time

def access_yt_channel(url, chrome_profile_path = "Profile 18"):
    print(f"Mở trình duyệt và truy cập: {url}")
    
    chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"  # Thay đổi nếu cần
    profile_arg = f"--profile-directory={chrome_profile_path}"
    
    subprocess.run([chrome_path, profile_arg, url])
    
    time.sleep(4.5)

def get_video_path(folder_dir): #get video inside folder path -- > handle changed file name case
    exts = {'.mp4','.mkv','.avi','.mov','.flv','.webm','.m4v'}
    return next((p for p in Path(folder_dir).iterdir() if p.is_file() and p.suffix.lower() in exts), None)


def split_dir(dir):
    #split_dir folder and filename
    folder = os.path.dirname(dir)
    filename = os.path.basename(dir)

    return folder, filename


def choose_file(folder_dir, file_name):

        x, y= 1626,56
        print(f'Move to {x,y}')
        pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad) 
        pyautogui.click()
        random_delay()
        #enter folder
        pyperclip.copy(folder_dir)
        pyautogui.hotkey("ctrl", "v")
        pyautogui.hotkey("enter")

        x, y= 1885,56
        print(f'Move to {x,y}')
        pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad) 
        pyautogui.click()
        random_delay()

        random_delay()
        #enter filename
        pyperclip.copy(file_name)
        pyautogui.hotkey("ctrl", "v")
        pyautogui.hotkey("enter")
        random_delay(2,3)

        #select file
        select_x, select_y = 303,156
        print(f'Move to {select_x, select_y}')
        pyautogui.moveTo(select_x, select_y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad)  
        pyautogui.click()
        random_delay()

        pyautogui.hotkey('enter')
        time.sleep(5)
        ##########################################################################
    
def ad_suitability():
    random_delay()
    #ad suitability
    x, y =1434, 399
    pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad)
    pyautogui.mouseDown()
    pyautogui.moveTo(x, y+800, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad) 
    pyautogui.mouseUp()
    time.sleep(random.uniform(1,2))

    location = pyautogui.locateOnScreen("img_data/confirm_content.png", confidence=0.7)
    if location:
        x, y = pyautogui.center(location) 
        pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad)
        random_delay()
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

    x,y = random.uniform(1369,1401), random.uniform(940,955)

    print(f'Move to {x,y}')
    pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad)
    random_delay()
    pyautogui.click()
    random_mouse()

def get_tag_name(html):
    soup = BeautifulSoup(html, 'html.parser')
    tag = soup.find('yt-formatted-string')
    if tag:
        return tag.text.strip()
    return None

def select_channel(channel_tag, total_channel):
    #go to def tool

    time.sleep(2)
    first_channel = [453,287]
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
        
def add_endscreen(level):
    x,y = 1345,545
    if level == 4 or level == 2:
        y += 210
    print(f'Move to {x,y}')
    pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad) 
    pyautogui.click()
    
    time.sleep(2)

    x,y = 625,385
    print(f'Move to {x,y}')
    pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad) 
    pyautogui.click()

    #modify
    x,y = 1400, 790
    pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad)
    pyautogui.mouseDown()
    pyautogui.moveTo(x+50, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad)
    pyautogui.mouseUp()

    x,y = 1400, 820
    pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad)
    pyautogui.mouseDown()
    pyautogui.moveTo(x+50, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad)
    pyautogui.mouseUp()

    x,y = 1400, 757
    pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad)
    pyautogui.mouseDown()
    pyautogui.moveTo(x+50, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad)
    pyautogui.mouseUp()

    #save
    x,y = 1385,230
    print(f'Move to {x,y}')
    pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad) 
    pyautogui.click()
    time.sleep(1)

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
