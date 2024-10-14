import csv
import json
import random
import glob
import os
from textwrap import indent

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


def csv_to_json(input_csv_filepaths, output_json_file):
  json_data = []

  for input_csv_filepath in input_csv_filepaths:
    with open(input_csv_filepath, 'r', newline='', encoding='utf-8') as csvfile:
      csvreader = csv.reader(csvfile)
      rows = list(csvreader)

      for idx, row in enumerate(rows):
        for caption in row[1:]:
          tmp = {
              'audio': f'clothocaption/{row[0]}',
              'conversations': [
                  {
                      'from': 'human',
                      'value': random.choice(question_seeds),
                      'input_modality': 'audio'
                  },
                  {
                      'from': 'gpt',
                      'value': f'{caption}',
                      'output_modality': 'text'
                  }
              ]
          }

          json_data.append(tmp)

  with open(output_json_file, 'w', encoding='utf-8') as f:
    # json.dump(json_data, f, ensure_ascii=False, indent=4) 
    json.dump(json_data, f, ensure_ascii=False, separators=(',', ':'))


if __name__ == '__main__':
  # 获取所有需要处理的CSV文件
  input_csv_filepaths = glob.glob('csvfiles/cn/*.csv')

  # 输出的JSON文件
  output_json_file = 'json/clothocaption_cn.json'
  csv_to_json(input_csv_filepaths, output_json_file)
