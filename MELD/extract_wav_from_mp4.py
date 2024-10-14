import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

# 设置日志记录
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def extract_audio(mp4_file, output_folder):
  # 保留原始文件名，将文件保存到新的文件夹中
  wav_file = os.path.join(output_folder, os.path.splitext(
      os.path.basename(mp4_file))[0] + ".wav")
  try:
    # 使用 ffmpeg 提取音频，采样率设置为 16000
    command = [
        'ffmpeg', '-i', mp4_file, '-vn', '-acodec', 'pcm_s16le',
        '-ar', '16000', '-ac', '2', wav_file, '-loglevel', 'quiet'
    ]
    # 运行命令行
    subprocess.run(command, check=True)
    # logging.info(f"成功提取音频: {wav_file}")
  except subprocess.CalledProcessError as e:
    logging.error(f"提取音频失败: {mp4_file}, 错误: {str(e)}")


def process_videos_in_folder(folder_path, output_folder, num_threads=2):
  # 如果输出文件夹不存在，则创建它
  if not os.path.exists(output_folder):
    os.makedirs(output_folder)

  # 获取文件夹中所有的 mp4 文件
  mp4_files = [os.path.join(folder_path, f)
               for f in os.listdir(folder_path) if f.endswith('.mp4')]

  # 使用线程池进行并发处理
  with ThreadPoolExecutor(max_workers=num_threads) as executor:
    future_to_file = {executor.submit(
        extract_audio, mp4_file, output_folder): mp4_file for mp4_file in mp4_files}
    for future in as_completed(future_to_file):
      file = future_to_file[future]
      try:
        future.result()
      except Exception as e:
        logging.error(f"{file} 处理过程中出错: {str(e)}")


if __name__ == "__main__":
  # 指定视频文件夹路径
  folder_path = "dev_splits"  # 替换为你的文件夹路径
  output_folder = "dev_wav"  # 替换为你想保存的文件夹路径
  process_videos_in_folder(folder_path, output_folder)
