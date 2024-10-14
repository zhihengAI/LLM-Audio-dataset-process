import json
import random
from concurrent.futures import ThreadPoolExecutor

# 定义线程数
THREAD_COUNT = 4

# 读取 JSON 文件
def read_json_file(file_path):
  with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)
  return data

# 随机化数据
def shuffle_data(data):
  random.shuffle(data)
  return data

# 写入 JSON 文件
def write_json_file(file_path, data):
  with open(file_path, 'w', encoding='utf-8') as file:
    # json.dump(data, file, ensure_ascii=False, indent=4)
    json.dump(data, file, ensure_ascii=False, separators=(',', ':'))
  print(f"Data written to {file_path}")

# 主函数
def main():
  file1 = 'TUT_Acoustic_scenes_ch.json'
  file2 = 'TUT_Acoustic_scenes_eng.json'
  output_file = 'TUT_Acoustic_scenes.json'

  with ThreadPoolExecutor(max_workers=THREAD_COUNT) as executor:
    future1 = executor.submit(read_json_file, file1)
    future2 = executor.submit(read_json_file, file2)

    data1 = future1.result()
    data2 = future2.result()

  combined_data = data1 + data2
  print(f"Combined data length before shuffling: {len(combined_data)}")

  shuffled_data = shuffle_data(combined_data)
  print(f"Combined data length after shuffling: {len(shuffled_data)}")

  write_json_file(output_file, shuffled_data)


if __name__ == "__main__":
  main()
