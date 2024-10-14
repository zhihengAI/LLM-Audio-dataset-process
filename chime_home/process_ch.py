import os
import csv
import json
import random
import concurrent.futures

question_seeds = [
    '这个音频中有什么声音？',
    '你能听到这个音频中有什么声音吗？',
    '这个音频中有哪些声音？',
    '这个音频里有什么声音出现？',
    '根据音频，你能听出什么声音吗？',
    '音频里有什么声音？',
    '这个音频中的声音是什么？',
    '你能确定这个音频里有什么声音吗？',
    '音频中能听到什么声音？',
    '这个音频中有什么特定的声音？',
    '音频里能听到什么声音？',
    '这个音频中能识别出什么声音吗？',
    '你能分辨出这个音频中有什么声音吗？',
    '音频中出现了什么声音？',
    '这个音频中有什么声音发出？',
    '听这个音频，你能听到什么声音？',
    '这个音频里能听到什么声音？',
    '音频中有什么声音可以被识别？',
    '你能从音频中辨别出什么声音吗？',
    '音频里能听出什么声音？',
    '这个音频中有什么声响？',
    '听音频，你能听到什么声响？',
    '这个音频里有什么声音发出？',
    '音频中出现了什么声音？',
    '这个音频中有什么声响？',
    '你能听到这个音频里的声音吗？',
    '音频里能听到什么声响？',
    '这个音频中的声音有哪些特征？',
    '音频中能辨别出什么声音吗？',
]


answer_seeds = [
    '根据音频中的人声和物体声音特征，可以推测这段音频中有',
    '通过分析音频中的声音元素，可以判断这段音频中有',
    '从音频中的特定声音来看，这段音频中有',
    '根据音频捕捉到的声音，可以推测这段音频中包含',
    '结合音频中的声音特征，可以判断这段音频中涉及',
    '从音频中的声音细节来看，可以听出这段音频中有',
    '根据音频中的人声和物体声，可以推测这段音频中存在',
    '通过对音频中的声音进行分析，可以判断这段音频中有',
    '从音频中的声音特征分析，可以听出这段音频中包含',
    '根据音频中的声音线索，可以推断这段音频中有',
    '鉴于音频中的声音特征，可以推测这段音频中有',
    '从音频中的人声和物体声音来看，这段音频中包含',
    '结合音频中的声音元素，可以判断这段音频中有',
    '根据音频中的特定声音，可以推测这段音频中有',
    '通过分析音频中的声音细节，可以判断这段音频中包含',
    '从音频捕捉到的声音特征来看，这段音频中有',
    '根据音频中的声音特征，可以推断这段音频中有',
    '从音频中的声音线索来看，这段音频中有',
    '通过对音频中的声音进行分析，可以推测这段音频中有',
    '根据音频中的背景音和物体声音，可以判断这段音频中包含',
    '从音频中的人声和物体互动音来看，这段音频中有',
    '结合音频中的声音细节，可以推测这段音频中有',
    '根据音频中的声音内容，可以推断这段音频中有',
    '通过分析音频中的各种声音元素，可以判断这段音频中有',
    '从音频中的声音特征分析，可以推测这段音频中有',
    '根据音频中的人声和物体声，可以推断这段音频中有',
    '结合音频中的声音线索，可以判断这段音频中包含',
    '从音频捕捉到的声音来看，这段音频中有',
    '通过分析音频中的声音细节，可以推测这段音频中有',
    '根据音频中的背景音和互动音，可以判断这段音频中有',
]

no_answer_seeds = [
    '在这段音频中没有检测到任何明显的声音。',
    '该音频不包含任何可识别的声音。',
    '这段音频中没有声音。',
    '此音频没有任何可检测到的声音。',
    '分析结果显示这段音频中没有声音。',
    '该音频是静音的，没有包含任何声音。',
    '在这段音频录音中未发现任何声音。',
    '这段音频似乎完全是静音的。',
    '这段音频中没有任何可听见的元素。',
    '在这段音频中未识别出任何声音事件。',
    '此音频没有产生任何噪音。',
    '该音频中没有任何声音。',
    '在这段音频中听不到任何声音。',
    '录音中不包含任何声音。',
    '这段音频片段是空的，没有声音。',
    '在这段音频中未检测到任何听觉信号。',
    '此音频是静音的，没有声音存在。',
    '在这段音频中未发现任何声学事件。',
    '这段音频录音完全是静音的。',
    '这段音频中没有噪声元素。',
    '该音频中不包含任何声音。',
    '这个音不包含任何声音。',
    '在录音中未检测到任何音频信号。',
    '该音频录音是静音的，没有声音。',
    '在这段音频中未发现任何声学信号。',
    '声音分析显示这段音频中是静音的。',
    '此音频中不包含任何声音。',
    '在这段音频中没有可辨别的声音。',
    '这段音频录音中没有声音。',
    '该音频是静音的，没有检测到任何声音。'
]

translation_dict = {
    'c': ['儿童说话声', '小孩的声音', '孩子的说话声'],
    'm': ['成年男性说话声', '男人的声音', '成年男子的说话声'],
    'f': ['成年女性说话声', '女人的声音', '成年女子的说话声'],
    'v': ['电子游戏/电视声', '电子设备发出的声音'],
    'p': ['打击声', '敲击或撞击的声音', '脚步声或撞击声'],
    'b': ['家用电器发出的声音', '家电的声音', '电器的声音'],
    'o': ['一些背景音', '环境音', '背景噪音']
}


def translate_majorityvote(vote):
  translated_elements = [
      random.choice(translation_dict[char])
      for char in vote if char in translation_dict
  ]
  return '、'.join(translated_elements)


def process_csv_file(csv_file):
  majorityvote = ""
  chunkname = ""

  with open(csv_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
      if row[0] == 'majorityvote':
        majorityvote = row[1]
      if row[0] == 'chunkname':
        chunkname = row[1]

  if random.random() < 0.6:
    answer_seed = ''
  else:
    answer_seed = random.choice(answer_seeds)

  translated_cv = translate_majorityvote(majorityvote)

  gpt_value = f'{answer_seed}{translated_cv}'
  if not translated_cv:
    gpt_value = random.choice(no_answer_seeds)

  json_data = {
      "audio": f"chime_home/{chunkname}.16kHz.wav",
      "conversations": [
          {
              "from": "human",
              "value": random.choice(question_seeds),
              "input_modality": "audio"
          },
          {
              "from": "gpt",
              "value": f'{gpt_value}。',
              "output_modality": "text"
          }
      ]
  }
  return json_data


def main(folder_path, output_json_path):
  csv_files = [os.path.join(folder_path, file) for file in os.listdir(
      folder_path) if file.endswith('.csv')]
  json_results = []

  # 使用多线程处理文件
  with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
    futures = {executor.submit(process_csv_file, csv_file)               : csv_file for csv_file in csv_files}
    for future in concurrent.futures.as_completed(futures):
      csv_file = futures[future]
      try:
        json_data = future.result()
        json_results.append(json_data)
        # print(f"Processed {csv_file} successfully.")
      except Exception as exc:
        print(f"Error processing {csv_file}: {exc}")

  with open(output_json_path, 'w', encoding='utf-8') as f:
    # json.dump(json_results, f, ensure_ascii=False, indent=4)
    json.dump(json_results, f, ensure_ascii=False, separators=(',', ':'))


# 执行主函数
if __name__ == "__main__":
  folder_path = "chunks"
  main(folder_path, 'json/chime_home_ch.json')
