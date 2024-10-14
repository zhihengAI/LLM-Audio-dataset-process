import os
import threading

# 全局变量，用于统计删除的文件数
deleted_count = 0
# 创建一个线程锁
lock = threading.Lock()


def delete_48khz_files(directory):
  global deleted_count
  for root, dirs, files in os.walk(directory):
    for file in files:
      if file.endswith('.wav'):
        file_path = os.path.join(root, file)
        try:
          os.remove(file_path)
          with lock:
            deleted_count += 1
          print(f"Deleted: {file_path}")
        except Exception as e:
          print(f"Error deleting {file_path}: {e}")


def main(directory):
  threads = []
  num_threads = 1

  # 启动多线程删除文件
  for i in range(num_threads):
    thread = threading.Thread(target=delete_48khz_files, args=(directory,))
    threads.append(thread)
    thread.start()

  for thread in threads:
    thread.join()

  print(f"Total files deleted: {deleted_count}")


if __name__ == "__main__":
  directory = "Raw JL corpus (unchecked and unannotated)/JL(wav+txt)"  # 将此路径替换为你的目标文件夹路径
  main(directory)
