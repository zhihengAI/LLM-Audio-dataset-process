import json
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

question_seeds = [
    "这个音频中有什么乐器演奏吗？",
    "音频中是什么乐器演奏？",
    "这个声音是什么乐器？",
    "能听到什么乐器在这个音频中演奏吗？",
    "音频中演奏的乐器是什么？",
    "这个声音源于什么乐器的演奏？",
    "这段音频里有乐器演奏吗？",
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


# 定义字典映射，包含每个instrument_family_str的三种翻译
translation_dict = {
    "reed": ["簧片", "簧管", "簧乐器"],
    "mallet": ["敲击乐器", "槌乐器", "打击乐器"],
    "keyboard": ["键盘乐器", "电子琴"],
    "guitar": ["吉他", "六弦琴", "拨弦乐器"],
    "organ": ["管风琴", "风琴", "电子管风琴"],
    "bass": ["贝斯", "低音吉他"],
    "brass": ["铜管乐器", "金属乐器"],
    "string": ["弦乐器", "拉弦乐器"],
    "flute": ["长笛", "横笛", "吹奏乐器"],
    "vocal": ["人声", "声乐音乐"],
    "synth_lead": ["合成主音", "合成音色"]
}

# 线程安全的list和锁
result_list = []
lock = Lock()


def process_item(key, value):
  """处理单个键值对，生成新的JSON项"""
  instrument_family_str = value.get("instrument_family_str")
  translated_labels = random.choice(translation_dict[instrument_family_str])

  if random.random() < 0.6:
    answer_seed = f'{translated_labels}'
  else:
    answer_seed = f'{random.choice(answer_seeds)}{translated_labels}的声音'

  new_item = {
      "audio": f"Nsynth/{key}.wav",
      "conversations": [
          {
              "from": "human",
              "value": random.choice(question_seeds),
              "input_modality": "audio"
          },
          {
              "from": "gpt",
              "value": f'{answer_seed}。',
              "output_modality": "text"
          }
      ]
  }
  with lock:
    result_list.append(new_item)
    # print(f"Processed {key}")


def main(json_file_path, output_file_path):
  # 读取并解析JSON文件
  with open(json_file_path, 'r') as file:
    data = json.load(file)

  # 使用ThreadPoolExecutor进行多线程处理
  with ThreadPoolExecutor(max_workers=8) as executor:
    futures = [executor.submit(process_item, key, value)
               for key, value in data.items()]

    # 等待所有线程完成
    for future in as_completed(futures):
      future.result()

  # 将结果保存到新的JSON文件中
  with open(output_file_path, 'w', encoding='utf-8') as out_file:
    #json.dump(result_list, out_file, ensure_ascii=False, indent=4)
    json.dump(result_list, out_file, ensure_ascii=False, separators=(',', ':'))

  print(f"New JSON file saved to {output_file_path}")


# 运行主函数
if __name__ == "__main__":
  json_file_path = "examples.json"  # 替换为你的JSON文件路径
  output_file_path = "json/Nsynth_aqa_ch.json"  # 替换为你希望保存的新JSON文件路径
  main(json_file_path, output_file_path)
