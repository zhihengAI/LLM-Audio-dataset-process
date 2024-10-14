import os
import json
import random
import threading

question_seeds = [
    '分析这段音频的内容。',
    '详细描述下这段音频。',
    '描述下这段音频。',
    '描述下这个音频。',
    '解析一下这段音频的内容。',
    '给我说说这段音频的具体内容。',
    '帮我解读一下这段音频的内容。',
    '这段音频的主要内容是什么？',
    '详细说明一下这段音频的内容。',
    '具体说说这段音频里的内容。',
    '分析一下这段音频。',
    '给我详细解释下这段音频的内容。',
    '解读一下这段音频的细节。',
    '详细描述一下这段音频的主要信息。',
    '这段音频的内容是什么？具体描述下。',
    '请详细分析这段音频。',
    '帮我解释一下这段音频的详细内容。',
    '这段音频的详细内容是什么？',
    '详细解读一下这段音频。',
    '说说这段音频的具体内容。',
    '这段音频的内容具体是什么？描述一下。',
    '请详细分析这段音频里的信息。',
    '具体解释一下这段音频的内容。',
    '详细说说这段音频的内容是什么。',
    '解析一下这段音频的具体内容。',
    '详细分析一下这段音频。',
    '详细描述下这段音频的每个细节。',
    '请你详细说明这段音频的内容。',
    '你能详细描述一下这段音频吗？',
    '具体解析一下这段音频的内容。',
    '详细讲解这段音频的每个细节。',
    '请描述这段音频的全部内容。',
    '帮我分析一下这段音频的内容。',
    '详细解释这段音频里的所有信息。',
    '请详细描述一下这段音频。',
    '具体描述一下这段音频的细节。',
    '详细说明这段音频里的内容。'
]

# 定义instrument_family_str到中文的翻译映射
translation_dict = {
    "bass": ["低音吉他", "贝司"],
    "drums": ["敲鼓", "打击乐器"],
    "vocals": ["人在歌唱", "纯人声"],
    "other": ["其他", "杂音", "背景音"],
    "mixture": ["歌手在歌唱", "音乐", "歌曲"]
}


def process_file(file_path, folder_name, results):
  instrument = os.path.splitext(os.path.basename(file_path))[
      0]  # 获取文件名作为instrument
  translated_labels = random.choice(
      translation_dict.get(instrument, ["未知"]))  # 获取随机翻译

  answer_seed = f'有{translated_labels}的声音。'

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
              "value": f'{answer_seed}',
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
  with open("json/musdb18hq_caption_test_ch.json", "w", encoding="utf-8") as f:
    # json.dump(results, f, ensure_ascii=False, indent=4)
    json.dump(results, f, ensure_ascii=False, separators=(',', ':'))

  print("Processing complete. Results saved to output.json")


if __name__ == "__main__":
  main()
