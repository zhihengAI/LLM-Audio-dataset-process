import json
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

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

  if random.random() < 0.5:
    answer_seed = f'{translated_labels}在演奏。'
  else:
    answer_seed = f'有{translated_labels}的声音。'

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
              "value": f'{answer_seed}',
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
    # json.dump(result_list, out_file, ensure_ascii=False, indent=4)
    json.dump(result_list, out_file, ensure_ascii=False, separators=(',', ':'))

  print(f"New JSON file saved to {output_file_path}")


# 运行主函数
if __name__ == "__main__":
  json_file_path = "examples.json"  # 替换为你的JSON文件路径
  output_file_path = "json/Nsynth_caption_ch.json"  # 替换为你希望保存的新JSON文件路径
  main(json_file_path, output_file_path)
