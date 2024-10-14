import os
import shutil
import concurrent.futures

threads = 8


def copy_and_replace_parentheses(file_name, source_folder):
  # 检查文件名是否包含 ( 和 )
  if '(' in file_name or ')' in file_name:
    # 替换文件名中的 ( 和 ) 为 _
    new_name = file_name.replace('(', '_').replace(')', '_')

    # 源文件路径
    source_file = os.path.join(source_folder, file_name)
    # 目标文件路径
    target_file = os.path.join(source_folder, new_name)

    try:
      # 复制并重命名文件
      shutil.copy2(source_file, target_file)
      print(f"Copied and renamed: {file_name} -> {new_name}")
    except Exception as e:
      print(f"Failed to copy {file_name}: {str(e)}")


def process_files(source_folder):
  # 获取文件夹下所有文件
  files = [f for f in os.listdir(source_folder) if os.path.isfile(
      os.path.join(source_folder, f))]

  # 使用多线程进行文件处理
  with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
    executor.map(lambda f: copy_and_replace_parentheses(
        f, source_folder), files)


if __name__ == "__main__":
  # 示例调用，传入目标文件夹路径
  folder_path = 'audio_files'  # 替换为实际的文件夹路径
  process_files(folder_path)
