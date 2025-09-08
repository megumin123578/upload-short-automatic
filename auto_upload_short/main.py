from module import *
import os
import pyautogui
import traceback
import pyperclip
from datetime import datetime


FOLDERS_LOG = 'folders.log'
PROGRESS_FILE = 'progress.txt'
VIDEOS_PER_BATCH = 3
MAX_VIDEOS_PER_FOLDER = 15
VIDEO_EXTS = ['.mp4', '.mov', '.avi', '.mkv']
DA_UP_FOLDER_NAME = '1. ĐÃ UP'  # Tên thư mục chứa các thư mục đã up


#config pyautogui
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.2

#data for video
publish_hour = ['7:00 PM', '03:00 AM', '09:00 AM']



access_yt_channel('https://studio.youtube.com/channel/UCnZVD65a5zSsmrDwzs9uzEg')
#go to channel select page
time.sleep(3)
x,y = random.uniform(836,945),random.uniform(655,676)
print(f"Move to ({x}, {y})")
pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad)  
pyautogui.click()
random_delay()  
random_mouse()

time.sleep(5)

#select channel
x_channel, y_channel = select_channel('@mgguymer',23) ###select_channel###
#turn off dev tool and select right channel
pyautogui.hotkey('f12')
print(f"Move to ({x_channel}, {y_channel})")
pyautogui.moveTo(x_channel, y_channel, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad)  
random_delay()
pyautogui.click()

x,y = random.uniform(1237,1289), random.uniform(620,645)
print(f"Move to ({x}, {y})")
pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad) 
random_delay() 
pyautogui.click()
    
random_delay(3,4)

create_video(0)


videos = get_next_video(MAX_VIDEOS_PER_FOLDER, DA_UP_FOLDER_NAME, VIDEOS_PER_BATCH)


#ghi vao file log
with open('log.txt', 'a', encoding='utf-8') as f:
    #write date time
    f.write(f'{datetime.now()}\n')
    for v in videos:
        f.write(f'{v}\n')
    f.write('\n')

count = 1
if videos:
    print("Video batch: ")
    for i,v in enumerate(videos):
        #loop through each video
        print(f'working on video: {v}')

        if i>0:
            create_video(i)

        folder, filename = split_dir(v)
        choose_file(folder,filename)

        #handling details
        x,y = random.uniform(956,1055), random.uniform(379,407)
        print(f"Move to ({x}, {y})")
        pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad) 
        random_delay() 
        pyautogui.click()
        
        #1 choose fourth video
        x,y = random.uniform(1028,1170), random.uniform(390,550)
        print(f"Move to ({x}, {y})")
        pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad) 
        random_delay(1,2) 
        pyautogui.click()

        #2wait
        time.sleep(random.randint(2,3))

        x,y = random.uniform(1225,1276), random.uniform(939,961)
        print(f"Move to ({x}, {y})")
        pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad) 
        random_delay() 
        pyautogui.click()

        #3copy title
        x,y = random.uniform(559,1026), random.uniform(452,475)
        print(f"Move to ({x}, {y})")
        pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad) 
        random_delay() 
        pyautogui.click()
        pyautogui.hotkey('ctrl','a')
        pyautogui.hotkey('ctrl','c')
        time.sleep(0.3)  
        title = pyperclip.paste()  #get data from clipboard
        new_title = increase_hash_number(title)
        pyperclip.copy(new_title)
        time.sleep(2)
        pyautogui.hotkey('ctrl','v')

        random_mouse()
        #click in empty space
        x,y = random.uniform(1500,1600), random.uniform(737,896)
        print(f"Move to ({x}, {y})")
        pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad) 
        random_delay() 
        pyautogui.click()
        time.sleep(1)

        #description
        x,y = random.uniform(561,999), random.uniform(623,640)
        print(f"Move to ({x}, {y})")
        pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad) 
        random_delay() 
        pyautogui.click()
        pyautogui.hotkey('ctrl','a')
        pyautogui.hotkey('ctrl','c')
        time.sleep(0.3)  
        description = pyperclip.paste()  #get data from clipboard
        new_des = increase_hash_number(description)
        pyperclip.copy(new_des)
        time.sleep(2)
        pyautogui.hotkey('ctrl','v')
        

        random_mouse()
        #click in empty space
        x,y = random.uniform(1500,1600), random.uniform(737,896)
        print(f"Move to ({x}, {y})")
        pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad) 
        random_delay() 
        pyautogui.click()
        time.sleep(1)


        #ad suitability
        x,y = random.uniform(721,840), random.uniform(300,357)
        print(f"Move to ({x}, {y})")
        pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad) 
        random_delay(1,2) 
        pyautogui.click()

        random_mouse()

        ad_suitability()

        x,y = random.uniform(1321,1364), random.uniform(482,511)
        print(f"Move to ({x}, {y})")
        pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad) 
        random_delay(1,2) 
        pyautogui.click()

        
        x,y = random.uniform(861,1005), random.uniform(348,497)
        print(f"Move to ({x}, {y})")
        pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad) 
        random_delay(1,2) 
        pyautogui.click()


        # go straight to schedule part

        time.sleep(4)
        x,y = random.uniform(1261,1379), random.uniform(298,357)
        print(f"Move to ({x}, {y})")
        pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad) 
        random_delay() 
        pyautogui.click()

        x, y =1428, 399
        pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad)
        pyautogui.mouseDown()
        pyautogui.moveTo(x, y+800, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad) 
        pyautogui.mouseUp()
        time.sleep(random.uniform(1,2))

        x,y = random.uniform(542,1047), random.uniform(621,682)
        print(f"Move to ({x}, {y})")
        pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad) 
        random_delay() 
        pyautogui.click()

        #Set schedule
        hour = publish_hour[i]
        today, tomorrow = get_date()
        #select_date
        if i == 0:
            #today
            date = today
        elif i>0:
            #tomorrow   
            date = tomorrow

        #set date
        x,y = random.uniform(558,715), random.uniform(600,635)
        print(f"Move to ({x}, {y})")
        pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad) 
        random_delay() 
        pyautogui.click()
        random_delay()
        pyautogui.hotkey('ctrl','a')
        pyperclip.copy(date)
        random_delay()
        pyautogui.hotkey('ctrl','v')
        random_delay()
        pyautogui.hotkey('enter')

        
        #set hour
        x,y = random.uniform(748,840), random.uniform(603,633)
        print(f"Move to ({x}, {y})")
        pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad) 
        random_delay() 
        pyautogui.click()
        random_delay()
        pyautogui.hotkey('ctrl','a')
        pyperclip.copy(hour)
        random_delay()
        pyautogui.hotkey('ctrl','v')
        random_delay()
        pyautogui.hotkey('enter')
        random_mouse()

        #upload
        x,y = random.uniform(1329,1406), random.uniform(945,973)
        print(f"Move to ({x}, {y})")
        pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad) 
        random_delay() 
        pyautogui.click()
       
        #close window

        x,y = random.uniform(1098,1153), random.uniform(656,685)
        print(f"Move to ({x}, {y})")
        pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad) 
        random_delay() 
        pyautogui.click()
        random_close = random.randint(1,2)
        if random_close == 1:
        
            x,y = random.uniform(1164,1195), random.uniform(419,445)
            print(f"Move to ({x}, {y})")
            pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad) 
            random_delay(2,3) 
            pyautogui.click()

        else:
            x,y = random.uniform(1131,1180), random.uniform(725,748)
            print(f"Move to ({x}, {y})")
            pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad) 
            random_delay(2,3) 
            pyautogui.click()

        count += 1

    
        time.sleep(random.uniform(20,30))
        
        

time.sleep(450)
pyautogui.hotkey('ctrl','w')
random_delay(1,2)
pyautogui.hotkey('ctrl','w')
