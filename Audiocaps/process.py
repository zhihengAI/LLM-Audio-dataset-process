import pandas as pd
import json
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

# 示例问题和回答种子，可以在实际使用时替换为真实数据
# question_seeds = [
#     '分析这段音频的内容。',
#     '详细描述下这段音频。',
#     '解析一下这段音频，内容要详细。',
#     '给我说说这段音频的具体内容。',
#     '帮我解读一下这段音频的内容。',
#     '这段音频的主要内容是什么？描述一下。',
#     '详细说明一下这段音频的内容。',
#     '具体说说这段音频里的内容。',
#     '分析一下这段音频，细节多些。',
#     '给我详细解释下这段音频的内容。',
#     '解读一下这段音频的细节。',
#     '详细描述一下这段音频的主要信息。',
#     '这段音频的内容是什么？具体描述下。',
#     '请详细分析这段音频。',
#     '帮我解释一下这段音频的详细内容。',
#     '这段音频的详细内容是什么？',
#     '详细解读一下这段音频。',
#     '说说这段音频的具体内容。',
#     '这段音频的内容具体是什么？描述一下。',
#     '请详细分析这段音频里的信息。',
#     '具体解释一下这段音频的内容。',
#     '详细说说这段音频的内容是什么。',
#     '解析一下这段音频的具体内容。',
#     '详细分析一下这段音频。',
#     '详细描述下这段音频的每个细节。',
#     '请你详细说明这段音频的内容。',
#     '你能详细描述一下这段音频吗？',
#     '具体解析一下这段音频的内容。',
#     '详细讲解这段音频的每个细节。',
#     '请描述这段音频的全部内容。',
#     '帮我分析一下这段音频的内容。',
#     '详细解释这段音频里的所有信息。',
#     '请详细描述一下这段音频。',
#     '具体描述一下这段音频的细节。',
#     '详细说明这段音频里的内容。'
# ]

question_seeds = [
    'Analyze the content of this audio.',
    'Describe this audio in detail.',
    'Analyze this audio, and be detailed.',
    'Tell me the specific content of this audio.',
    'Help me interpret the content of this audio.',
    'What is the main content of this audio? Describe it.',
    'Explain the content of this audio in detail.',
    'Specifically describe the content of this audio.',
    'Analyze this audio with more details.',
    'Give me a detailed explanation of the content of this audio.',
    'Interpret the details of this audio.',
    'Describe the main information of this audio in detail.',
    'What is the content of this audio? Describe it specifically.',
    'Please analyze this audio in detail.',
    'Help me explain the detailed content of this audio.',
    'What is the detailed content of this audio?',
    'Interpret this audio in detail.',
    'Tell me the specific content of this audio.',
    'What is the specific content of this audio? Describe it.',
    'Please analyze the information in this audio in detail.',
    'Specifically explain the content of this audio.',
    'Tell me in detail what the content of this audio is.',
    'Analyze the specific content of this audio.',
    'Analyze this audio in detail.',
    'Describe each detail of this audio in detail.',
    'Please explain the content of this audio in detail.',
    'Can you describe this audio in detail?',
    'Specifically analyze the content of this audio.',
    'Explain each detail of this audio in detail.',
    'Please describe all the content of this audio.',
    'Help me analyze the content of this audio.',
    'Explain all the information in this audio in detail.',
    'Please describe this audio in detail.',
    'Specifically describe the details of this audio.',
    'Explain the content of this audio in detail.'
]

# 处理每一行的函数


def process_row(row):
  audiocap_id = row['audiocap_id']
  caption = row['caption']

  # 构造JSON数据
  data = {
      "audio": f"audiocaps/val/{audiocap_id}.wav",
      "conversations": [
          {
              "from": "human",
              "value": random.choice(question_seeds),
              "input_modality": "audio"
          },
          {
              "from": "gpt",
              "value": caption,
              "output_modality": "text"
          }
      ]
  }

  return data

# 多线程处理CSV文件的函数


def process_csv(file_path, num_threads=8):
  # 读取CSV文件
  df = pd.read_csv(file_path)

  # 保存处理后的数据
  json_results = []

  # 使用 ThreadPoolExecutor 进行多线程处理
  with ThreadPoolExecutor(max_workers=num_threads) as executor:
    futures = {executor.submit(process_row, row)               : index for index, row in df.iterrows()}

    for future in as_completed(futures):
      index = futures[future]
      try:
        result = future.result()
        json_results.append(result)
        print(f"Processed row {index + 1}/{len(df)}")
      except Exception as e:
        print(f"Error processing row {index + 1}: {e}")

  return json_results

# 保存JSON数据到文件的函数


def save_json(data, output_file):
  with open(output_file, 'w', encoding='utf-8') as f:
    #json.dump(data, f, ensure_ascii=False, indent=4)
    json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
  print(f"JSON file saved as {output_file}")


# 主程序入口
if __name__ == "__main__":
  csv_file_path = "val.csv"  # 替换成你的csv文件路径
  output_json_file = "audiocaps_eng_val.json"

  # 处理CSV文件，生成JSON数据
  json_data = process_csv(csv_file_path)

  # 保存JSON数据到文件
  save_json(json_data, output_json_file)
