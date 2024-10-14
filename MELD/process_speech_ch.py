import csv
import json
import os
import random
import glob
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm  # 引入 tqdm 库
import chardet


question_seeds = [
    '这段音频中说话的人说了什么？',
    '音频中的说话者在说什么？',
    '从音频中可以听出说话者说了什么？',
    '这段音频里说话者说了哪些内容？',
    '音频中的说话者表达了什么内容？',
    '听了这段音频后，你能听出说话者说了什么吗？',
    '通过这段音频，判断说话者在说什么？',
    '这段音频中，说话者的具体内容是什么？',
    '音频里能听出说话者说了什么吗？',
    '音频中说话者表达的内容是什么？',
    '这段音频中，能听出说话者在表达什么吗？',
    '从音频中，你能辨别出说话者说了什么内容吗？',
    '这段音频里的说话者在说些什么？',
    '通过音频中的声音，可以知道说话者在说什么吗？',
    '音频中的说话者在表达什么内容？',
    '这段音频中说话者的发言内容是什么？',
    '音频里说话者在表达什么？',
    '通过这段音频，可以听出说话者说了什么内容吗？',
    '音频中的说话者传递了什么样的信息？',
    '这段音频中，能听出说话者的讲话内容吗？',
    '音频里说话者说的具体是什么？',
    '这段音频中说话者说了些什么？',
    '通过这段音频，能听出说话者在说什么吗？',
    '这段音频中说话者的讲话内容是什么？',
    '你能从这段音频中听出说话者在说什么吗？',
]


answer_seeds = [
    '从音频里能听出，说话者',
    '从音频可以判断出，说话人',
    '从音频中可以听出来，说话',
    '从音频的内容中可以明显听出，说话人',
    '从音频中可以听到，说话者',
    '从音频里可以得知，说话人',
    '从音频中可以确定，说话者',
    '从音频中清晰地表明，说话人',
    '从音频听来，可以听出，说话者',
    '从音频的内容中，可以听到说话人',
    '从录音中可以听出，说话者',
    '从音频中可以听出，说话人',
    '从音频的语气中可以听到，说话者',
    '从音频的内容里可以听出，说话人',
    '从音频中可以识别出，说话者',
    '从音频的声音里，可以听到说话人',
    '从音频中可以很明显地听出，说话者',
    '从音频中可以分辨出，说话人',
    '从音频里可以直接得知，说话者',
    '从音频的对话中可以听出，说话者',
    '从音频中可以完整听到，说话人'
]


def read_csv_annotations(csv_file):
  annotations = []
  with open(csv_file, mode='rb') as csvfile:
    result = chardet.detect(csvfile.read())
    csvencoding = result['encoding']
    print('encoding: ', csvencoding)

  with open(csv_file, newline='', encoding=csvencoding) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      annotations.append(row)
  return annotations


def process_audio_file(file_path, annotation, base_dir):
  # 获取文件名（不带路径）
  fname = os.path.basename(file_path)
  # 获取情绪并随机选择一个中文翻译
  utterance = annotation['Utterance']

  answer_seed = random.choice(answer_seeds)
  if random.random() < 0.6:
    answer_seed = '说话者在说'

  # 构建JSON数据
  json_data = {
      "audio": f"MELD/{base_dir}/{fname}",
      "conversations": [
          {
              "from": "human",
              # 忽略 question_seeds，这里直接给一个例子
              "value": random.choice(question_seeds),
              "input_modality": "audio"
          },
          {
              "from": "gpt",
              "value": f'{answer_seed} \"{utterance}\" 这句话。',
              "output_modality": "text"
          }
      ]
  }

  return json_data

# 处理一个 .csv 文件和对应的 .wav 文件夹，将结果追加到 results 列表中


def process_csv_and_wav(csv_file, wav_folder, results):
    # 判断是 train 还是 dev
  base_dir = "train" if "train" in csv_file else "dev"

  # 读取CSV文件
  annotations = read_csv_annotations(csv_file)

  # 获取所有.wav文件并排序
  wav_files = sorted(glob.glob(os.path.join(wav_folder, '*.wav')))

  # 检查注解和.wav文件数量，裁剪到相同的长度
  min_length = min(len(annotations), len(wav_files))
  annotations = annotations[:min_length]
  wav_files = wav_files[:min_length]

  # 使用ThreadPoolExecutor进行多线程处理，添加进度条
  with ThreadPoolExecutor(max_workers=8) as executor:
    future_to_file = {executor.submit(
        process_audio_file, file_path, annotations[i], base_dir): file_path for i, file_path in enumerate(wav_files)}
    for future in tqdm(future_to_file, desc=f"Processing {wav_folder}", total=len(future_to_file)):
      result = future.result()
      results.append(result)

  print(f"All files in {wav_folder} processed.")

# 主函数，处理多个 .csv 和 .wav 文件夹，并将结果合并保存到一个JSON文件中


def main(csv_files, wav_folders, output_json_file):
  results = []

  for csv_file, wav_folder in zip(csv_files, wav_folders):
    process_csv_and_wav(csv_file, wav_folder, results)

  # 将所有结果保存到一个JSON文件中
  with open(output_json_file, 'w', encoding='utf-8') as json_file:
    # json.dump(results, json_file, ensure_ascii=False, indent=4)
    json.dump(results, json_file, ensure_ascii=False, separators=(',', ':'))

  print(f"All data saved to {output_json_file}")


if __name__ == "__main__":
  # csv_files = ["dev_sent_emo.csv", "train_sent_emo.csv"]  # 替换为你的CSV文件路径列表
  # wav_folders = ["dev_wav", "train_wav"]    # 替换为你的.wav文件夹路径列表
  csv_files = ["train_sent_emo.csv"]
  wav_folders = ["train_wav"]
  output_json_file = "json/MELD_speech_ch.json"                   # 合并后的JSON文件名
  main(csv_files, wav_folders, output_json_file)
