import os
import json
import random
import threading

question_seeds = [
    "这个音频中有什么乐器演奏吗？",
    "音频中是什么乐器演奏？",
    "这个声音是什么乐器？",
    "能听到什么乐器在这个音频中演奏吗？",
    "音频中演奏的乐器是什么？",
    "这个声音源于什么乐器的演奏？",
    "这段音频中的乐器是什么？",
    "能确定这个音频里的乐器吗？",
    "这个音频里的声音来自于什么乐器？",
    "在这个音频中，演奏的乐器是什么？",
    "音频里能听到什么乐器的声音？",
    "这个音频中的乐器是哪个？",
    "你能听出这个音频中的乐器吗？",
    "这个声音是由什么乐器发出的？",
    "你能识别出音频中的乐器演奏吗？",
    "音频中传达的是什么乐器的声音？",
    "这个音频里的乐器是啥？",
    "可以辨认出音频中的乐器吗？",
    "这段音频里有什么乐器在演奏？",
    "在这个音频里，你能听到什么乐器？",
    "音频中的乐器演奏是什么？",
    "这个音频的乐器声音来自哪里？",
    "能识别出这个音频里的乐器吗？",
    "音频里传来的乐器是什么？",
    "你能听到这个音频中的乐器演奏吗？",
    "这段音频中主要的乐器是什么？",
    "这个音频中演奏的是哪种乐器？",
    "能听出这段音频中的乐器种类吗？",
    "这个音频里发出的乐器声音是什么？"
]

answer_seeds = [
    "可以从这个音频中听出是",
    "从这个音频中可以听出是",
    "可以从这段音频中听出是",
    "从这段音频中可以听出是",
    "可以从这个录音中听出是",
    "从这个录音中可以听出是",
    "可以从这段录音中听出是",
    "从这段录音中可以听出是",
    "可以从这个声音中听出是",
    "从这个声音中可以听出是",
    "可以从这段声音中听出是",
    "从这段声音中可以听出是",
    "可以从这个片段中听出是",
    "从这个片段中可以听出是",
    "可以从这段片段中听出是",
    "从这段片段中可以听出是",
    "可以从这个音轨中听出是",
    "从这个音轨中可以听出是",
    "可以从这段音轨中听出是",
    "从这段音轨中可以听出是"
]

# 定义instrument_family_str到中文的翻译映射
translation_dict = {
    "bass": ["低音吉他", "贝司"],
    "drums": ["鼓", "打击乐器"],
    "vocals": ["人在歌唱", "纯人声"],
    "other": ["其他", "杂音", "背景音"],
    "mixture": ["歌手在歌唱", "音乐", "歌曲"]
}


def process_file(file_path, folder_name, results):
  instrument = os.path.splitext(os.path.basename(file_path))[
      0]  # 获取文件名作为instrument
  translated_labels = random.choice(
      translation_dict.get(instrument, ["未知"]))  # 获取随机翻译

  if random.random() < 0.6:
    answer_seed = f'{translated_labels}'
  else:
    answer_seed = f'{random.choice(answer_seeds)}{translated_labels}的声音'

  # 构造JSON对象
  data = {
      "audio": f"musdb18hq/{folder_name}/{instrument}.wav",
      "conversations": [
          {
              "from": "human",
              "value": random.choice(question_seeds),  # 忽略 question_seeds
              "input_modality": "audio"
          },
          {
              "from": "gpt",
              "value": f'{answer_seed}。',
              "output_modality": "text"
          }
      ]
  }
  results.append(data)  # 将结果添加到列表中
  # print(f"Processed: {file_path}")  # 打印处理信息

# 定义主函数，遍历文件夹并进行多线程处理


def main():
  base_dir = "test"
  results = []
  threads = []

  for root, dirs, files in os.walk(base_dir):
    for file in files:
      if file.endswith(".wav"):
        if 'other' in file or 'mixture' in file:
          continue
        folder_name = os.path.relpath(root, base_dir)
        file_path = os.path.join(root, file)

        # 创建并启动新线程
        thread = threading.Thread(
            target=process_file, args=(file_path, folder_name, results))
        threads.append(thread)
        thread.start()

        # 限制线程数
        if len(threads) >= 8:
          for thread in threads:
            thread.join()  # 等待线程完成
          threads = []

  # 等待所有线程完成
  for thread in threads:
    thread.join()

  # 保存结果到JSON文件
  with open("json/musdb18hq_aqa_test_ch.json", "w", encoding="utf-8") as f:
    #json.dump(results, f, ensure_ascii=False, indent=4)
    json.dump(results, f, ensure_ascii=False, separators=(',', ':'))

  print("Processing complete. Results saved to output.json")


if __name__ == "__main__":
  main()
