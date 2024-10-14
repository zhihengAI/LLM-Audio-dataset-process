import csv
import os

# 读取CSV文件
csv_filename = 'clotho_captions_evaluation.csv'  # 请将此处替换为你的CSV文件名
with open(csv_filename, 'r') as csvfile:
    reader = csv.reader(csvfile)
    filenames = [row[0] for row in reader]
  
# 遍历文件名并重命名
for i, filename in enumerate(filenames[1:-1]):
    old_filepath = os.path.join('evaluation', filename)  # 请将此处替换为你的音频文件目录
    new_filename = f'evaluation_{i}.wav'
    new_filepath = os.path.join('evaluation', new_filename)
    
    if os.path.exists(old_filepath):
        os.rename(old_filepath, new_filepath)
        print(f'Renamed: {old_filepath} to {new_filepath}')
    else:
        print(f'File not found: {old_filepath}')
