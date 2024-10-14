import csv
import json
import os
import random
import glob
from concurrent.futures import ThreadPoolExecutor
import chardet
from tqdm import tqdm  # 引入 tqdm 库

question_seeds = [
    '这段音频里面说话的人的语气情绪如何？',
    '音频中的说话者是用什么样的语气情绪在说话？',
    '分析音频中的声音，说话人的语气情绪是怎样的？',
    '从音频中的语气情绪，可以推测出说话者的情绪。',
    '音频中说话人的语气情绪给人什么样的感觉？',
    '听了这段音频后，判断说话者的语气情绪是什么样的。',
    '这段音频中说话者表达了什么情绪？',
    '通过音频中的语气情绪，可以得出说话者的情绪是什么？',
    '音频中的说话者传递了什么样的情绪？',
    '这段音频中，能感受到说话者的情绪吗？',
    '从这段音频中，判断说话者的情绪是什么？',
    '通过音频中的语气情绪，识别说话者的情绪。',
    '这段音频中的说话者情绪如何？',
    '这段音频中说话者的情绪特征是什么？',
    '音频中能听出说话者的情绪吗？',
    '音频中的说话者是用怎样的语气情绪在讲话？',
    '音频里说话者的语气情绪反映了什么样的情绪？',
    '通过这段音频，判断说话者是用什么情绪在表达？',
    '音频中说话者的语气情绪表现了什么情绪？',
    '这段音频中说话者的情绪是什么样的？',
    '音频中的说话者用什么样的情绪在表达？',
    '从音频中可以听出说话者的情绪是怎样的？',
    '通过这段音频，判断说话者的情绪。',
    '音频中，能听出说话者在表达什么情绪吗？',
    '说话者在音频中的情绪如何？'
]

answer_seeds = [
    '听音频可以感受到，说话者',
    '通过音频可以判断出，说话者',
    '从音频里能听出，说话者',
    '从音频可以感觉到，说话者',
    '听这段音频时，可以听出来，说话者',
    '通过这段音频，可以明显听出，说话者',
    '音频中传达出，说话者',
    '从这段录音中可以感受到，说话者',
    '听完音频，可以得出，说话者',
    '音频中清晰地表明，说话者',
    '听这段录音，可以推测出，说话者',
    '从这段音频听来，可以发现，说话者',
    '从音频的声音中，可以察觉到，说话者',
    '通过音频的语调，可以听出，说话者',
    '从音频内容中，可以辨别出，说话者',
    '通过这段音频的声音，可以听出，说话者',
    '从音频的细节中可以感知到，说话者',
    '听完这段音频，你会注意到，说话者',
    '音频中透露出，说话者',
    '从录音中不难听出，说话者',
    '通过音频的语气情绪，可以听出，说话者',
    '这段音频让人感觉到，说话者',
    '听这段音频，可以感觉到，说话者',
    '通过这段录音，可以明确地感知到，说话者',
    '从音频的内容来看，可以听出，说话者',
    '通过音频的表达方式，可以判断出，说话者',
    '从录音中清晰地感受到，说话者',
    '听这段录音时，会发现，说话者',
    '通过音频中的语调变化，可以听出，说话者',
    '从这段音频的语气情绪中，可以感受到，说话者',
]

# 情绪到中文翻译的字典映射
emotion_dict = {
    'anger': ['愤怒的', '生气的', '恼怒的', '愠怒的'],
    'disgust': ['厌恶的', '反感的', '憎恶的', '恶心的'],
    'fear': ['恐惧的', '害怕的', '畏惧的', '恐慌的'],
    'joy': ['快乐的', '高兴的', '愉快的', '喜悦的'],
    'neutral': ['中立的', '平静的', '冷静的', '淡定的'],
    'sadness': ['悲伤的', '难过的', '忧伤的', '伤心的'],
    'surprise': ['惊讶的', '惊奇的', '意外的', '惊愕的']
}


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
  emotion = annotation['Emotion']
  translated_emotion = random.choice(emotion_dict[emotion])

  answer_seed = random.choice(answer_seeds)
  if random.random() < 0.6:
    answer_seed = ''
  answer_seed += '情绪是'

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
              "value": f'{answer_seed}{translated_emotion}。',
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
    #json.dump(results, json_file, ensure_ascii=False, indent=4)
    json.dump(results, json_file, ensure_ascii=False, separators=(',', ':'))

  print(f"All data saved to {output_json_file}")


if __name__ == "__main__":
  # csv_files = ["dev_sent_emo.csv", "train_sent_emo.csv"]  # 替换为你的CSV文件路径列表
  # wav_folders = ["dev_wav", "train_wav"]    # 替换为你的.wav文件夹路径列表
  csv_files = ["train_sent_emo.csv"]
  wav_folders = ["train_wav"]
  output_json_file = "json/MELD_emo_ch.json"                   # 合并后的JSON文件名
  main(csv_files, wav_folders, output_json_file)
