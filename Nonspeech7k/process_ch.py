import os
import csv
import json
import random
import threading
from concurrent.futures import ThreadPoolExecutor

# 线程数
THREAD_COUNT = 8


# 模拟的种子
question_seeds = [
    '这个音频中的人物在干什么？',
    '音频里的人物在做什么？',
    '你能听出音频中的人物在干什么吗？',
    '这段音频里的人物在进行什么动作？',
    '根据音频，你能猜出人物在做什么吗？',
    '音频中的人物在从事什么行为？',
    '这段音频中，人物在进行什么样的动作？',
    '听音频，你能识别出人物在干什么吗？',
    '音频里的人物正在做什么事情？',
    '这段音频中的人物正在做什么？',
    '音频中能听出人物的行为是什么吗？',
    '这个音频中，人物的动作是什么？',
    '听音频，你能确定人物在做什么吗？',
    '音频里的人物正在进行什么操作？',
    '音频中的人物在干啥？',
    '这段音频中，你能判断人物在做什么吗？',
    '你能根据音频判断人物的动作吗？',
    '音频中的人物行为是什么？',
    '这个音频里的人物正在干什么？',
    '这段音频里能听出人物在进行什么行为吗？',
    '音频中人物的行为是什么？',
    '音频中的人物在从事什么活动？',
    '听音频，你能辨别出人物的行为吗？',
    '音频里的人物正在做什么事情？',
    '音频中的人物在干些什么？',
    '这个音频里人物的动作是什么？',
    '听音频，你能推断出人物在做什么吗？',
    '音频中人物的行为动作是什么？',
    '音频里人物在做什么？'
]

answer_seeds = [
    '根据音频中的声音特征，可以推测人物正在',
    '通过分析音频中的声音，可以判断人物在',
    '从音频中的声音来看，人物在',
    '根据音频捕捉到的声音，可以推测人物正在',
    '结合音频中的声音细节，可以判断人物在',
    '从音频中的声音特征分析，可以听出人物在',
    '根据音频中的声音，可以推测人物正在',
    '通过对音频中的声音分析，可以判断人物在',
    '从音频中的声音细节来看，可以听出人物正在',
    '根据音频中的声音线索，可以推断人物正在',
    '鉴于音频中的声音特征，可以推测人物正在',
    '从音频中的声音来看，人物正在',
    '结合音频中的声音元素，可以判断人物在',
    '根据音频中的声音，可以推测人物正在',
    '通过分析音频中的声音细节，可以判断人物在',
    '从音频捕捉到的声音来看，人物可能在',
    '根据音频中的声音特征，可以推断人物正在',
    '从音频中的声音线索来看，人物正在',
    '通过对音频中的声音分析，可以推测人物正在',
    '从音频中的声音来听，人物正在',
    '结合音频中的声音细节，可以推测人物在',
    '根据音频中的声音内容，可以推断人物正在',
    '通过分析音频中的各种行为声音元素，可以判断人物在',
    '从音频中的声音特征分析，可以推测人物正在',
    '根据音频中的声音，可以推断人物正在',
    '结合音频中的声音线索，可以判断人物在',
    '从音频捕捉到的声音来看，人物可能正在',
    '通过分析音频中的声音细节，可以推测人物在',
    '根据分析音频，可以判断人物正在',
]

# Classname翻译字典
translated_cv = {
    "breath": ["呼吸", "喘气", "吸气", "呼气"],
    "cough": ["咳嗽", "轻微咳嗽", "干咳", "干咳嗽"],
    "crying": ["哭泣", "流泪", "抽泣", "啜泣"],
    "laugh": ["笑", "大笑", "咯咯笑"],
    "screaming": ["尖叫", "大声尖叫", "惊恐尖叫", "高声喊叫"],
    "sneeze": ["打喷嚏", "轻微喷嚏", "连续喷嚏"],
    "yawn": ["打哈欠", "张口哈欠"],
    "yawm": ["打哈欠", "张口哈欠"]
}


def process_csv_file(csv_path, combined_data):
  parent_path_name = "test" if "test" in csv_path else "train"

  with open(csv_path, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)

    for row in reader:
      filename = row["Filename"]
      classname = row["Classname"]

      # 获取翻译列表，如果classname不在字典中，则返回包含原始classname的列表
      translations = translated_cv.get(classname, [classname])
      # 从翻译列表中随机选择一个翻译
      translated_classname = random.choice(translations)

      answer_seed = f'{random.choice(answer_seeds)}'
      if random.random() < 0.6:
        answer_seed = ''

      # 构建JSON数据
      json_data = {
          "audio": f"Nonspeech7k/{parent_path_name}/{filename}",
          "conversations": [
              {
                  "from": "human",
                  "value": random.choice(question_seeds),
                  "input_modality": "audio"
              },
              {
                  "from": "gpt",
                  "value": f'{answer_seed}{translated_classname}。',
                  "output_modality": "text"
              }
          ]
      }

      # 将构建好的数据添加到combined_data列表中
      combined_data.append(json_data)


def get_csv_files(directory):
  csv_files = []
  for root, _, files in os.walk(directory):
    for file in files:
      if file.endswith(".csv"):
        csv_files.append(os.path.join(root, file))
  return csv_files

# 主函数


def main():
  base_dir = "."
  csv_files = get_csv_files(base_dir)

  combined_data = []

  with ThreadPoolExecutor(max_workers=THREAD_COUNT) as executor:
    futures = []
    for csv_file in csv_files:
      futures.append(executor.submit(
          process_csv_file, csv_file, combined_data))

    # 等待所有线程完成
    for future in futures:
      future.result()

  # 将所有数据写入一个JSON文件
  with open("json/Nonspeech7K_ch.json", "w", encoding="utf-8") as outfile:
    # json.dump(combined_data, outfile, ensure_ascii=False, indent=4)
    json.dump(combined_data, outfile,
              ensure_ascii=False, separators=(',', ':'))

  print("All data have beed combined")


if __name__ == "__main__":
  main()
