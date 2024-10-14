import os
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
    json.dump(data, file, ensure_ascii=False, separators=(',', ':'))
  print(f"Data written to {file_path}")

# 获取指定文件夹中的所有 JSON 文件


def get_json_files(directory):
  json_files = []
  for root, dirs, files in os.walk(directory):
    for file in files:
      if file.endswith('.json'):
        json_files.append(os.path.join(root, file))
  return json_files

# 主函数


def main():
  input_directory = '.'  # 替换为你JSON文件所在的文件夹路径
  output_file = 'audiocaps_eng.json'

  json_files = get_json_files(input_directory)

  if not json_files:
    print("No JSON files found in the specified directory.")
    return

  print(f"Found {len(json_files)} JSON files.")

  with ThreadPoolExecutor(max_workers=THREAD_COUNT) as executor:
    futures = [executor.submit(read_json_file, file) for file in json_files]

    combined_data = []
    for future in futures:
      data = future.result()
      combined_data.extend(data)

  print(f"Combined data length before shuffling: {len(combined_data)}")

  shuffled_data = shuffle_data(combined_data)
  print(f"Combined data length after shuffling: {len(shuffled_data)}")

  write_json_file(output_file, shuffled_data)


if __name__ == "__main__":
  main()
