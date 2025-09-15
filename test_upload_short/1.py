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


last_channel = 'abc'
def same_channel(channel):
    return last_channel == channel

print(same_channel('abc'))
last_channel = '567'
print(same_channel('abc'))