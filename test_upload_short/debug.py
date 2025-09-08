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
        print(f'Working on: title: {title}, description: {description}, video_directory: {vid_dir}, channel: {channel}')

        try:
            #false url
            youtube_url = 'https://studio.youtube.com/channel/UCnZVD65a5zSsmrDwzs9uzEg'

            #handle channel url
            channel_df = pd.read_csv('short_channels.csv')
            config = channel_df[channel_df['channel'] == channel].iloc[0]
            #asign value
            tag_name = config['tag_name']
            numbers_of_playist = int(config['numbers_of_playlist'])
            
            access_yt_channel(youtube_url)

            folder, filename = split_dir(vid_dir) #file mp4 location
            video_path = get_video_path(folder) 
            folder, filename = split_dir(video_path)

            #go to channel select page
            upload_vid_to_right_channel(tag_name)
            choose_file(folder, filename)

            insert_title_and_description(title, description)


   

    #         #set for kids
    #         if for_kids == 'Yes':
    #             x,y = 540,692
    #             print(f'Move to {x,y}')
    #             pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.5), tween=pyautogui.easeInOutQuad) 
    #             pyautogui.click()
    #         else:
    #             x,y = 540,726
    #             print(f'Move to {x,y}')
    #             pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.5), tween=pyautogui.easeInOutQuad) 
    #             pyautogui.click()

            
    #         if level == 2:
    #             #move to monetization
    #             x,y = random.uniform(1366,1402), random.uniform(938,961)
    #             print(f'Move to {x,y}')
    #             pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad) 
    #             random_delay()
    #             pyautogui.click()

    #             time.sleep(10)
    #             x,y = random.uniform(542,886), random.uniform(465,491)
    #             if for_kids == 'Yes':
    #                 time.sleep(100)
    #                 y=545
    #             print(f'Move to {x,y}')
    #             pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad) 
    #             random_delay()
    #             pyautogui.click()

    #             x,y = random.uniform(542,886), random.uniform(478,460)
    #             if for_kids == 'Yes':
                    
    #                 y=random.uniform(532,548)
    #             print(f'Move to {x,y}')
    #             pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad) 
    #             random_delay()
    #             pyautogui.click()

    #             x,y = random.uniform(863,893), random.uniform(553,573)
    #             if for_kids == 'Yes':
                    
    #                 y=random.uniform(633,651)
    #             print(f'Move to {x,y}')
    #             pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad) 
    #             random_delay()
    #             pyautogui.click()

    #             x,y = random.uniform(1366,1402), random.uniform(938,961)
    #             print(f'Move to {x,y}')
    #             pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad) 
    #             random_delay()
    #             pyautogui.click()

    #             #ad suitability
    #             ad_suitability()

    #             #######################END SCREEN#############################################
    #             #video cho trẻ em
    #             if for_kids == 'Yes': #dont have endscreen 
    #                 x,y = 1386,955
    #                 print(f'Move to {x,y}')
    #                 pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad)
    #                 random_delay()
    #                 pyautogui.click()
                    

    #             #video không cho trẻ em
    #             elif for_kids == 'No': # False 
    #                 #add endscreen
    #                 add_endscreen(level)
    #             if level == 1:
    #                 if for_kids == 'No':
    #                     #add endscreen
    #                     x,y = 1381, 955
    #                     print(f'Move to {x,y}')
    #                     pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad) 
    #                     pyautogui.click()
    #                     add_endscreen(level)
    #                 x,y = 1390, 960
    #                 print(f'Move to {x,y}')
    #                 pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad) 
    #                 pyautogui.click()
                    
    #         random_mouse()
    #         #####################################################################

    #         if level == 3 or level == 4:
    #             #move to monetization
    #             x,y = 1385,960
    #             print(f'Move to {x,y}')
    #             pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad) 
    #             random_delay()
    #             pyautogui.click()
                
    #             if len(add_territories) > 0:
    #                 time.sleep(random.uniform(1,2))
    #                 location = pyautogui.locateOnScreen("img_data/specific_territories.png", confidence=0.8)
    #                 if location:
    #                     x, y = pyautogui.center(location) 
    #                     pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad)  
    #                     print(x,y)
    #                     random_delay()
    #                     pyautogui.click()

    #                 x = random.uniform(627,1307)
    #                 y += random.uniform(120,128)
    #                 print(f'Move to {x,y}')
    #                 pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad) 
    #                 pyautogui.click()

    #                 time.sleep(1)
    #                 pyperclip.copy(add_territories)
    #                 random_delay()
    #                 pyautogui.hotkey('ctrl','v')

            


    #             x,y = 1434,478
    #             pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad)
    #             random_delay()
    #             pyautogui.mouseDown()
    #             pyautogui.moveTo(x, y+600, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad) 
    #             pyautogui.mouseUp()

    #             if len(add_territories) >0:
    #                 x,y = random.uniform(609, 800),544
    #                 print(f'Move to {x,y}')
    #                 pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad) 
    #                 pyautogui.click()

    #             random_mouse()
    #             x,y = 687,842
    #             print(f'Move to {x,y}')
    #             pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad) 
    #             pyautogui.click()
    #             pyperclip.copy(title)
    #             random_delay()
    #             pyautogui.hotkey('ctrl','v')


    #             x,y = 1376,946
    #             print(f'Move to {x,y}')
    #             pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad) 
    #             pyautogui.click()
    #             time.sleep(random.uniform(1,2))
    #             pyautogui.click()
    #             random_delay()
                
    #             #ad suitability
    #             ad_suitability()

                
                
    #             #######################END SCREEN#############################################
    #             #video cho trẻ em
    #             if for_kids == 'Yes': #dont have endscreen 
    #                 x,y = 1386,955
    #                 print(f'Move to {x,y}')
    #                 pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad)
    #                 random_delay()
    #                 pyautogui.click()
                    

    #             #video không cho trẻ em
    #             elif for_kids == 'No': # False 
    #                 #add endscreen
    #                 add_endscreen(level)
    #             if level == 1:
    #                 if for_kids == 'No':
    #                     #add endscreen
    #                     x,y = 1381, 955
    #                     print(f'Move to {x,y}')
    #                     pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad) 
    #                     pyautogui.click()
    #                     add_endscreen(level)
    #                 x,y = 1390, 960
    #                 print(f'Move to {x,y}')
    #                 pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad) 
    #                 pyautogui.click()
                    
    #         random_mouse()
    #         #####################################################################
    #         #next
    #         x,y = 1390, 960
    #         print(f'Move to {x,y}')
    #         pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad) 
    #         pyautogui.click()
    #         random_delay(1,2)
    #         print(f'Move to {x,y}')
    #         pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad) 
    #         pyautogui.click()

    #         #public stattus = không công khai
            
    #         x,y = 591, 532
    #         print(f'Move to {x,y}')
    #         pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad)
    #         pyautogui.click()

            

    #         if str(publish_hour) != 'nan':

    #             #scroll
    #             x,y = 1435,463
    #             print(f'Move to {x,y}')
    #             pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad)
    #             pyautogui.mouseDown()
    #             print(f'Move to {x,y+300}')
    #             pyautogui.moveTo(x, y+300, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad)
    #             pyautogui.mouseUp()

    #             #schedule
    #             x,y = 755, 645
    #             print(f'Move to {x,y}') #date
    #             pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad)
    #             pyautogui.click()
                
    #             x,y = 695, 580
    #             print(f'Move to {x,y}')
    #             pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad)
    #             pyautogui.click()
    #             pyperclip.copy(convert_date(publish_date))
    #             pyautogui.hotkey('ctrl','a')
    #             pyautogui.hotkey('ctrl','v')
    #             pyautogui.hotkey('enter')

    #             x, y = 772, 574 #hour
    #             print(f'Move to {x,y}')
    #             pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad)
    #             pyautogui.click()
    #             pyperclip.copy(publish_hour)
    #             pyautogui.hotkey('ctrl','a')
    #             pyautogui.hotkey('ctrl','v')
    #             pyautogui.hotkey('enter')
    #             #Done
    #             x,y = 1375,960
    #             print(f'Move to {x,y}')
    #             pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad)
    #             pyautogui.click()


    #             x,y = 1115,675
    #             print(f'Move to {x,y}')
    #             pyautogui.moveTo(x, y, duration=0.2, tween=pyautogui.easeInOutQuad)
    #             time.sleep(random.uniform(1,2))
    #             pyautogui.click()

    #         else:
    #             x,y = random.uniform(1385,1407), random.uniform(186,206)
    #             print(f'Move to {x,y}')
    #             pyautogui.moveTo(x, y, duration=0.2, tween=pyautogui.easeInOutQuad)
    #             time.sleep(random.uniform(1,2))
    #             pyautogui.click()

    #             x,y = random.uniform(1108,1177), random.uniform(631,659)
    #             print(f'Move to {x,y}')
    #             pyautogui.moveTo(x, y, duration=0.2, tween=pyautogui.easeInOutQuad)
    #             time.sleep(random.uniform(1,2))
    #             pyautogui.click()
    #         #     x,y = 1384,944
    #         #     print(f'Move to {x,y}')
    #         #     pyautogui.moveTo(x, y, duration=0.2, tween=pyautogui.easeInOutQuad)
    #         #     time.sleep(random.uniform(1,2))
    #         #     pyautogui.click()

    #         # # handling pop up after upload
    #         # time.sleep(2)
    #         # try:
    #         #     location = pyautogui.locateOnScreen('img_data/popup.PNG', confidence=0.7)
    #         #     if location:
    #         #         x,y = pyautogui.center(location)
    #         #         x+=69
    #         #         y+= 108
    #         #         print(f'Move to {x,y}')
    #         #         pyautogui.moveTo(x, y, duration=0.2, tween=pyautogui.easeInOutQuad)
    #         #         time.sleep(random.uniform(1,2))
    #         #         pyautogui.click()
    #         #     else:
    #         #         print("keep running")
    #         # except Exception as e:
    #         #     print("Khong tim thay cua so mo ra:", e)

    #         #update_exxcel
    #         full_df.at[idx, 'status'] = 'Uploaded'       
        
            
    #         full_df.to_excel(EXCEL_FILE, index=False, engine='openpyxl')
    #         random_mouse()
        except Exception as e:
            print(f"Lỗi xảy ra: {e}")

            traceback.print_exc()

        

    # #update sheet
    # excel_to_sheet(EXCEL_FILE, SHEET_NAME,sheet_idx)
    # return count
        
if __name__ == "__main__":
        
    while True:
        main(5)
        print("Start sleep", datetime.now())
        time.sleep(60)
        print("End sleep", datetime.now())
