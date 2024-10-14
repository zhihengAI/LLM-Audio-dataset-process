import os
import json
import random
import argparse
from concurrent.futures import ThreadPoolExecutor

# 定义线程数
THREAD_COUNT = 8


def read_json_file(file_path):
  with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)
  return data


def shuffle_data(data):
  random.shuffle(data)
  return data


def write_json_file(file_path, data):
  with open(file_path, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, separators=(',', ':'))
  print(f"Data written to {file_path}")


def get_json_files(directory):
  json_files = []
  for root, dirs, files in os.walk(directory):
    for file in files:
      if file.endswith('.json'):
        json_files.append(os.path.join(root, file))
  return json_files


def main(input_directory):
  output_file = os.path.join(input_directory, f'json/{input_directory}.json')

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
  parser = argparse.ArgumentParser(
      description="Process JSON files in a directory and shuffle their content.")
  parser.add_argument('--input_dir', type=str,
                      help='The directory containing JSON files to process.')

  args = parser.parse_args()

  main(args.input_dir)
