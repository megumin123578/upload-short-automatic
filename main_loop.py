import time
import subprocess
from datetime import datetime
import random
import pyautogui

while True:
    now = datetime.now()
    print(f"Chạy lúc: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    subprocess.run(['python', 'show_asmr_and_6789_satisfying.py'])

    for _ in range(2):
        time.sleep(random.randint(1900, 2500))
        pyautogui.hotkey('ctrl','w')
        time.sleep(random.uniform(1,2))
        pyautogui.hotkey('esc')