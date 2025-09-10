import pyautogui
import time
import pyperclip
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import random
import traceback
from module import *
from datetime import datetime
import sys

# Đảm bảo stdout/stderr là UTF-8 và không vỡ chương trình vì ký tự lạ
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

EXCEL_FILE = 'temp_upload.xlsx'
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
CREDS_FILE = r"C:\Users\Admin\Documents\main\Tuan_number\main_folder\sheet.json"
SHEET_NAME = "Auto_concat_vids"


# Cấu hình PyAutoGUI
pyautogui.FAILSAFE = True  
pyautogui.PAUSE = 0.2

timeout = 15 #max 15s wait browser

def main(sheet_idx):
    try:
        creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
        gc = gspread.authorize(creds)
        copy_from_ggsheet_to_excel(gc, SHEET_NAME, EXCEL_FILE, sheet_idx)

        filtered_df, full_df = pre_process_data(EXCEL_FILE)
        count = len(filtered_df)
        print(f'There are {count} videos need to be upload')
        

    except Exception as e:
        print(f"Error in main execution: {e}")
        return

    for idx, row in filtered_df.iterrows():
        title = row['Title']
        description = row['Description']
        vid_dir = clean_path(row['video directory'])
        channel = row['Channel']
        publish_hour = row['Publish hour']
        publish_date = row['Publish date']
        print(f'Working on: {title}, {vid_dir}, {channel}, {publish_hour}, {publish_date}')

        success = False  # cờ theo dõi kết quả

        for attempt in range(2):  # tối đa 2 lần
            try:
                youtube_url = 'https://studio.youtube.com/channel/UCnZVD65a5zSsmrDwzs9uzEg'

                # lấy config channel
                channel_df = pd.read_csv('short_channels.csv')
                config = channel_df[channel_df['channel'] == channel].iloc[0]
                tag_name = config['tag_name']
                numbers_of_playist = int(config['numbers_of_playlist'])

                access_yt_channel(youtube_url)

                folder, filename = split_dir(vid_dir)
                video_path = get_video_path(folder) 
                folder, filename = split_dir(video_path)

                upload_vid_to_right_channel(tag_name)
                choose_file(folder, filename)

                insert_title_and_description(title, description)
                add_to_playlist(numbers_of_playist)
                ad_suitability()
                related_vids()
                go_to_visibility()

                random_delay()
                url = publish(publish_hour, publish_date)

                full_df['URL'] = full_df['URL'].astype('string')

                if is_url(url):
                    full_df.at[idx, 'status'] = 'Uploaded'
                    full_df.at[idx, 'URL'] = url
                    success = True
                    print(f"Upload thành công ở lần thử {attempt+1}")
                    break  # ra khỏi vòng retry
                else:
                    raise ValueError("Publish không trả về URL hợp lệ")

            except Exception as e:
                print(f"Lỗi xảy ra lần {attempt+1}: {e}")
                traceback.print_exc()
                if attempt == 0:
                    print("Thử lại upload một lần nữa...")
                else:
                    full_df.at[idx, 'status'] = 'Failed'

            finally:
                # lưu excel sau mỗi lần thử
                full_df.to_excel(EXCEL_FILE, index=False, engine='openpyxl')
                random_mouse()
            
            time.sleep(60)
            pyautogui.hotkey('ctrl','w')
            random_delay()
            pyautogui.hotkey('ctrl','w')
            random_delay()
            pyautogui.hotkey('esc')
                

    if not success:
        print(f"Video {title} thất bại sau 2 lần thử")


        

    #update sheet
    excel_to_sheet(EXCEL_FILE, SHEET_NAME,sheet_idx)
    
        
if __name__ == "__main__":
        
    while True:
        main(5)

