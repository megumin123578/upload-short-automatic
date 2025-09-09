import random
import pyautogui
import pyperclip
from module import *

time.sleep(3)
#schedule
x,y = random.uniform(1006,1036), random.uniform(623,670)
print(f'Move to {x,y}') #date
pyautogui.moveTo(x, y, duration=random.uniform(0.3,0.4), tween=pyautogui.easeInOutQuad)
pyautogui.click()

random_delay(0.1,0.2)
pyautogui.hotkey('tab')
random_delay(0.1,0.2)
pyautogui.hotkey('enter')
pyperclip.copy(to_mmm_d_yyyy("10/9/2025"))
pyautogui.hotkey('ctrl','a')
pyautogui.hotkey('ctrl','v')
pyautogui.hotkey('enter')

random_delay(0.1,0.2)
pyautogui.hotkey('tab')
random_delay(0.1,0.2)
pyautogui.hotkey('tab')
pyperclip.copy("10:30")
pyautogui.hotkey('ctrl','a')
random_delay(0.1,0.2)
pyautogui.hotkey('ctrl','v')
random_delay(0.1,0.2)
pyautogui.hotkey('enter')
random_delay()
next_section() # publish


for _ in range(3):
    random_delay(0.1,0.2)
    pyautogui.hotkey('tab')
pyautogui.hotkey('enter')
url = pyperclip.paste()

#close
for _ in range(2):
    random_delay(0.1,0.2)
    pyautogui.hotkey('tab')
pyautogui.hotkey('enter')