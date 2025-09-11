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
from datetime import datetime
import subprocess
import time

def click(x1,x2,y1,y2):
    x,y = random.uniform(x1,x2), random.uniform(y1,y2)
    print(f'Move to {x,y}')
    pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad)
    random_delay()
    pyautogui.click()

def clean_path(p: str) -> str:
    """Làm sạch path lấy từ sheet/Excel để dùng được trên Windows."""
    if p is None:
        return ""
    s = str(p).strip()

    for z in ["\ufeff", "\u200b", "\u200c", "\u200d", "\u2060"]:
        s = s.replace(z, "")

    if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
        s = s[1:-1]
    else:
        s = s.strip('"').strip("'")

    s = s.replace("/", "\\").rstrip(" .")

    if s.startswith("//"):
        s = "\\" + s  # -> "\/..." rồi thay tiếp
    if s.startswith("\\/"):
        s = s.replace("\\/", "\\", 1)
    return s

def ends_with_tag(text: str) -> bool:
    text = text.strip()
    return bool(re.search(r"(?:^|\s)(#[\w]+)$", text))

def excel_to_sheet(excel_file, sheet_file, worksheet_index):
    df = pd.read_excel(excel_file, engine="openpyxl")

    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    CREDS_FILE = r"C:\Users\Admin\Documents\main\Tuan_number\main_folder\sheet.json"

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


def random_delay(min_sec = 0.5, max_sec = 1):
    time.sleep(random.uniform(min_sec, max_sec))

_MONTH_ABBR = ["", "Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
import re
def convert_date(input_date): #vietnamese date
    date_splited = input_date.split('/')
    pl_date = f'{date_splited[0]} thg {date_splited[1]}, 20{date_splited[2]}'
    return pl_date
def to_mmm_d_yyyy(s: str, dayfirst: bool = True) -> str:
    """
    - dayfirst=False: ưu tiên mm/dd/yyyy
    - dayfirst=True : ưu tiên dd/mm/yyyy
    """
    x = str(s).strip().strip('"').strip("'")
    x = re.sub(r"[.\-]", "/", x)  # chuẩn hóa dấu phân cách

    fmts_pref = ("%d/%m/%Y", "%m/%d/%Y") if dayfirst else ("%m/%d/%Y", "%d/%m/%Y")
    fmts = fmts_pref + ("%Y/%m/%d",)

    dt = None
    for fmt in fmts:
        try:
            dt = datetime.strptime(x, fmt)
            break
        except ValueError:
            continue
    if dt is None:
        raise ValueError(f"Không parse được ngày: {s}")

    return f"{_MONTH_ABBR[dt.month]} {dt.day}, {dt.year}"

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
        'Channel','Title','Description','video directory',
        'Publish hour','Publish date'
    ]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in Excel: {missing}. "
                        f"Check header spelling/casing/whitespace.")
    filtered_df = df[
        df['Channel'].notna() &
        df['video directory'].notna() &
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



def access_yt_channel(url, chrome_profile_path = "Profile 18"):
    print(f"Mở trình duyệt và truy cập: {url}")
    
    chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"  # Thay đổi nếu cần
    profile_arg = f"--profile-directory={chrome_profile_path}"
    
    subprocess.run([chrome_path, profile_arg, url])
    
    time.sleep(4.5)


def split_dir(dir):
    #split_dir folder and filename
    folder = os.path.dirname(dir)
    filename = os.path.basename(dir)

    return folder, filename


def choose_file(folder_dir, file_name):
        
        time.sleep(2)

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
        time.sleep(2)

        #select file
        select_x, select_y = 303,156
        print(f'Move to {select_x, select_y}')
        pyautogui.moveTo(select_x, select_y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad)  
        pyautogui.click()
        random_delay()

        pyautogui.hotkey('enter')
        time.sleep(5)
        ##########################################################################
    
def next_section():
    click(1369,1401,940,955)

def ad_suitability():

    #ad suitability
    scroll_max()

    location = pyautogui.locateOnScreen(r"C:\Users\Admin\Documents\dev\upload-short\test_upload_short\img_data\confirm_content.png", confidence=0.7)
    if location:
        x, y = pyautogui.center(location) 
        pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad)
        random_delay()
        pyautogui.click()
    random_delay()

    #send submit
    location = pyautogui.locateOnScreen(r"C:\Users\Admin\Documents\dev\upload-short\test_upload_short\img_data\send_submit.png", confidence=0.8)
    if location:
        x, y = pyautogui.center(location) 
        pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad)
        random_delay()
        pyautogui.click()
    random_delay()

    time.sleep(random.uniform(6,7))

    next_section()
    random_mouse()
    

def get_tag_name(html):
    soup = BeautifulSoup(html, 'html.parser')
    tag = soup.find('yt-formatted-string')
    if tag:
        return tag.text.strip()
    return None

def select_channel(channel_tag, total_channel):
    #go to def tool

    random_delay()
    first_channel = [453,287]
    x,y = first_channel[0], first_channel[1]
    
    first_time = 1
    for _ in range(total_channel):

        x += 300 #move x to seccond col
        pyautogui.hotkey('ctrl','shift','c')
        if first_time == 1:
            time.sleep(3)
            first_time -= 1
        else:
            time.sleep(1)
        random_delay(0.1,0.2 )
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
        random_delay() 
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
        random_delay() 
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

def upload_vid_to_right_channel(tag_name):

    click(836,945,648,676)
    random_delay()  
    random_mouse()
    random_delay()

    x_channel, y_channel = select_channel(tag_name,28) ###select_channel###
    #turn off dev tool and select right channel
    pyautogui.hotkey('f12')
    print(f"Move to ({x_channel}, {y_channel})")
    random_delay()
    pyautogui.moveTo(x_channel, y_channel, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad)  
    pyautogui.click()
    
    click(1237,1289,620,645)
        
    random_delay(3,4)

    #go to studio
    x,y =1856,148
    print(f"Move to ({x}, {y})")
    pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad)  
    pyautogui.click()
    time.sleep(6)

    location = pyautogui.locateOnScreen(r"C:\Users\Admin\Documents\dev\upload-short\test_upload_short\img_data\yt_studio.png", confidence=0.7)
    x,y = pyautogui.center(location)
    print(x, y)
    pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad) 
    pyautogui.click()

    time.sleep(6)

    location = pyautogui.locateOnScreen(r"C:\Users\Admin\Documents\dev\upload-short\test_upload_short\img_data\create_button.png", confidence=0.7)
    if location:
        x,y = pyautogui.center(location)
        print(x, y)
        pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad) 
        pyautogui.click()
    
    y = random.uniform(193,207)
    print(f'move to: {x, y}')
    pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad) 
    pyautogui.click()

    choose_vid_x, choose_vid_y = 960, 540
    print(f'Move to {choose_vid_x, choose_vid_y}')
    pyautogui.moveTo(choose_vid_x, choose_vid_y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad)  
    random_delay()
    pyautogui.click()
    random_delay()


def insert_title_and_description(channel, title, description):
    
    #reuse 
    click(961,1047,372,395)
    random_delay()
    #chose the second one
    click(701,826,378,533)
    time.sleep(2)
    #done
    location = pyautogui.locateOnScreen(r"C:\Users\Admin\Documents\dev\upload-short\test_upload_short\img_data\reuse.png", confidence=0.7)
    if location:
        x, y = pyautogui.center(location) 
        x += random.uniform(20,50)
        pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad)
        random_delay()
        pyautogui.click()
    random_mouse()
    
    random_delay()
    for _ in range(3):
        pyautogui.hotkey('tab')
        random_delay()
    # Title
    pyautogui.hotkey("ctrl", "a")
    random_delay()

    # if title is NaN or empty
    is_nan = (isinstance(title, float) and pd.isna(title)) or (str(title).strip().lower() == 'nan') or (str(title).strip() == '')

    if is_nan:
        print('Chưa đặt title, dùng title mặc định của kênh')
    else:
        pyperclip.copy(str(title))
        random_delay()
        pyautogui.hotkey("ctrl", "v")

    time.sleep(2)
    if channel == 'zzTESTzz':
        loop_nums = 3
        if ends_with_tag(title):
            loop_nums += 1
        for _ in range(loop_nums):
            pyautogui.hotkey('tab')
            random_delay()
        pyautogui.hotkey('enter')
        random_delay()
        pyautogui.hotkey('enter')

        click(541,1046,396,417)

    #move to description with tab
    random_delay()
    loop_nums = 2
    if ends_with_tag(title):
            loop_nums += 1
    for _ in range(loop_nums):
        pyautogui.hotkey('tab')
        random_delay()
    
    pyautogui.hotkey("ctrl", "a")
    random_delay(0.4, 0.5)
    if len(str(description)) > 5:
        pyperclip.copy(str(description))
        pyautogui.hotkey("ctrl", "v")
    
    next_section()

def scroll_max():
    time.sleep(2)
    x,y = 1434,478
    pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad)
    random_delay()
    pyautogui.click()
    random_delay()
    pyautogui.mouseDown()
    pyautogui.moveTo(x, y+999, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad) 
    pyautogui.mouseUp()

def add_to_playlist(channel, numbers_of_playist):
    #scroll max
    scroll_max()
    
        #open playlist select
    x,y = 650,410
    print(f'Move to {x,y}')
    pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.5), tween=pyautogui.easeInOutQuad) 
    random_delay()
    pyautogui.click()

        #check box
    if channel == 'zzTESTzz': #pass through search
        random_delay(0.2,0.3)
        pyautogui.hotkey('tab')

    random_delay(0.2,0.3)
    pyautogui.hotkey('tab')
    for _ in range(numbers_of_playist):
        pyautogui.hotkey('enter')
        random_delay(0.2,0.3)
        pyautogui.hotkey('down')
        random_delay(0.2,0.3)

    #done
    random_delay(0.2,0.3)
    pyautogui.hotkey('tab')
    random_delay(0.2,0.3)
    pyautogui.hotkey('tab')
    random_delay(0.2,0.3)
    pyautogui.hotkey('enter')

    random_delay()
    next_section()

def go_to_visibility():
    random_delay(0.2,0.4)
    time.sleep(100)
    next_section()

def related_vids(level):
    #select add
    random_delay()
    if level == 1:
        click(1329,1361,473,493)
    else:
        click(1329,1361,423,453)
        

    for _ in range(4):
        pyautogui.hotkey('tab')
        random_delay()

    for _ in range(random.randint(0,10)):
        random_delay()
        pyautogui.hotkey('tab')

    pyautogui.hotkey('enter')
    time.sleep(2)
    next_section()
def _is_missing(v):
    if v is None:
        return True
    if isinstance(v, float) and math.isnan(v):
        return True
    if isinstance(v, str) and v.strip().lower() in ("", "nan", "none"):
        return True
    return False

def is_url(s: str) -> bool:
    pattern = re.compile(
        r'^(https?://[^\s/$.?#].[^\s]*)$', re.IGNORECASE
    )
    return bool(pattern.match(s))

def publish(publish_hour, publish_date):
    time.sleep(2)
    scroll_max()
    if not _is_missing(publish_hour):

        #schedule
        click(1006,1036,623,652)
        random_delay()
        pyautogui.hotkey('tab')
        random_delay()
        pyautogui.hotkey('enter')
        random_delay()
        pyperclip.copy(to_mmm_d_yyyy(publish_date))
        pyautogui.hotkey('ctrl','a')
        random_delay()
        pyautogui.hotkey('ctrl','v')
        random_delay()
        pyautogui.hotkey('enter')
        
        #publish hour
        pyperclip.copy(publish_hour)
        random_delay()
        click(742,836,595,609)
        pyautogui.hotkey('ctrl','a')
        random_delay()
        pyautogui.hotkey('ctrl','v')
        random_delay()
        pyautogui.hotkey('enter')
        random_delay()

        next_section() # publish
        #close
        time.sleep(3)
        click(760,1154,681,692)
        
        random_delay()
        pyautogui.hotkey('tab')
        random_delay()
        pyautogui.hotkey('enter')

    else:
        next_section()