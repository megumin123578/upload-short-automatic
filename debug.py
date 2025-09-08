import random
import pyautogui
import time

time.sleep(2)
try:
    location = pyautogui.locateOnScreen('img_data/popup.PNG', confidence=0.8)
    if location:
        x,y = pyautogui.center(location)

        print(f'Move to {x,y}')
        pyautogui.moveTo(x, y, duration=0.2, tween=pyautogui.easeInOutQuad)
        time.sleep(random.uniform(1,2))
        pyautogui.click()
    else:
        print("keep running")
except Exception as e:
    print("Khong tim thay cua so mo ra:", e)