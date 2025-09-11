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

time.sleep(3)
# # Đảm bảo stdout/stderr là UTF-8 và không vỡ chương trình vì ký tự lạ
# if hasattr(sys.stdout, "reconfigure"):
#     sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# EXCEL_FILE = 'temp_upload.xlsx'
# SCOPES = [
#     "https://www.googleapis.com/auth/spreadsheets",
#     "https://www.googleapis.com/auth/drive"
# ]
# CREDS_FILE = r"C:\Users\Admin\Documents\main\Tuan_number\main_folder\sheet.json"
# SHEET_NAME = "Auto_concat_vids"


# # Cấu hình PyAutoGUI
# pyautogui.FAILSAFE = True  
# pyautogui.PAUSE = 0.2

# timeout = 15 #max 15s wait browser
# time.sleep(3)


# creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
# gc = gspread.authorize(creds)
# copy_from_ggsheet_to_excel(gc, SHEET_NAME, EXCEL_FILE, 5)

# filtered_df, full_df = pre_process_data(EXCEL_FILE)
# count = len(filtered_df)
# print(f'There are {count} videos need to be upload')

# for idx, row in filtered_df.iterrows():
#     title = row['Title']
#     description = row['Description']
#     vid_dir = clean_path(row['video directory'])
#     channel = row['Channel']
#     publish_hour = row['Publish hour']
#     publish_date = row['Publish date']

# channel_df = pd.read_csv('short_channels.csv')
# config = channel_df[channel_df['channel'] == channel].iloc[0]
# #asign value
# tag_name = config['tag_name']

# right_manager = config['right_manager']
# level = config['related_vid_level']

# insert_title_and_description(channel, title, description)
# related_vids(level)

click(1340,1364,600,630)