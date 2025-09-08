import pandas as pd

# Đọc file CSV
channel_df = pd.read_csv('channel_data.csv')

# Tên kênh đang cần lấy config
channel = 'Show ASMR'  # Hoặc thay bằng biến động

# Lấy dòng tương ứng
config = channel_df[channel_df['channel'] == channel].iloc[0]

# Gán giá trị
tag_name = config['tag_name']
numbers_of_playist = int(config['numbers_of_playlist'])
num_lines = int(config['num_lines'])
add_territories = config['add_territories'] if pd.notna(config['add_territories']) else ""
level = int(config['level'])
