import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

# 线程安全的set和锁
unique_instrument_families = set()
lock = Lock()


def process_item(item):
  """处理单个键值对，提取instrument_family_str"""
  global unique_instrument_families
  instrument_family_str = item.get("instrument_family_str")

  if instrument_family_str:
    with lock:
      unique_instrument_families.add(instrument_family_str)


def main(json_file_path):
  # 读取并解析JSON文件
  with open(json_file_path, 'r') as file:
    data = json.load(file)

  # 使用ThreadPoolExecutor进行多线程处理
  with ThreadPoolExecutor(max_workers=8) as executor:
    futures = [executor.submit(process_item, item) for item in data.values()]

    # 等待所有线程完成
    for future in as_completed(futures):
      future.result()

  # 打印所有unique的instrument_family_str值
  print("Unique instrument_family_str values:")
  for value in unique_instrument_families:
    print(value)


# 运行主函数
if __name__ == "__main__":
  json_file_path = "examples.json"  # 替换为你的JSON文件路径
  main(json_file_path)
