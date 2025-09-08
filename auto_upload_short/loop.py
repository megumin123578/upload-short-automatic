from datetime import datetime
import subprocess
import time

def get_latest_date(file_path):
    latest_date = None
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                date_str = line.split()[0]  
                date_obj = datetime.strptime(date_str, '%Y-%m-%d').date() 
                
                if not latest_date or date_obj > latest_date:
                    latest_date = date_obj
            except Exception as e:
                continue  

    return latest_date


file_path = 'log.txt'

while True:
    latest_date = get_latest_date(file_path)
    if latest_date:
        print(f"Ngày mới nhất trong file là: {latest_date}")
    else:
        print("Không tìm thấy ngày hợp lệ trong file.")
    #ktra xem up video cho hom nay chua
    current_date = datetime.now().date()  
    print(f"Ngày hôm nay là: {current_date}")
    if latest_date == current_date:
        print(f"Đã up video cho ngày hôm nay rồi !")
    else:
        print(f"Hôm nay chưa up video")

        #neu chua up
        now = datetime.now()

        #
        if now.hour * 60 + now.minute >= 0 * 60 + 30:
            print("Đang chạy upload short...")
            subprocess.run(['python', 'main.py'])
            
    now = datetime.now()
