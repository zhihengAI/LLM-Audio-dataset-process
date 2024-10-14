import csv
import json
import random
import threading
from concurrent.futures import ThreadPoolExecutor
import sys

question_seeds = [
    '这段音频中有哪些人物或者物体发出了声音？',
    '音频里有哪些人物或物体在发声？',
    '你能听出音频中的哪些人物或物体在发声吗？',
    '音频中出现了哪些人物或物体的声音？',
    '这段音频里的声音是由哪些人物或物体发出的？',
    '根据音频，你能识别出哪些人物或物体在发声吗？',
    '这段音频中有什么特定的人物或物体在发声？',
    '听这段音频，你能确定有哪些人物或物体在发声吗？',
    '这段音频中的人物或物体发出的声音是什么样的？',
    '音频中有哪些人物或物体在制造声音？',
    '这段音频里能听到哪些人物或物体的声音？',
    '音频中能识别出哪些人物或物体在发声吗？',
    '音频中有哪些人物或物体发出了噪音？',
    '这段音频中有哪些人物或物体的声音？',
    '你能分辨出音频中的哪些人物或物体在发声吗？',
    '音频里哪些人物或物体发出了声响？',
    '听音频，你能识别出哪些人物或物体在讲话吗？',
    '音频中哪些人物或物体发出了特殊的声响？',
    '音频里能听到哪些人物或物体的声音？',
    '音频中能辨别出哪些人物或物体在发声吗？',
    '这段音频中人物或物体的声音有哪些特征？',
    '音频中有哪些人物或物体在制造噪音？',
    '音频里你能听出哪些人物或物体在发声吗？',
    '这段音频中有哪些物体的声音和哪些人物的声音？',
    '音频中能识别出哪些人物或物体的声音吗？',
    '音频里什么人物或物体在发出声响？',
    '听音频，你能分辨出哪些人物或物体的声音吗？',
    '音频中有什么人物或物体在制造声响？',
    '这段音频里哪些人物或物体的声音可以被识别？',
    '你能从音频中辨别出哪些人物或物体在发声吗？',
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

nosound_seeds = [
    '这段音频中没有检测到任何人物或物体的声音。',
    '根据音频分析，没有发现任何明显的声音。',
    '这段音频里没有捕捉到任何明显的声响。',
    '音频中没有识别到人物或物体发出的声音。',
    '这段音频中没有检测到有声响。',
    '通过分析音频，没有发现声音的存在。',
    '从音频中未检测到任何人物或物体的声音。',
    '音频中没有听到任何声音。',
    '根据音频，没有发现任何声源。',
    '这段音频里没有识别到任何声音。',
    '音频分析结果显示没有检测到声音。',
    '通过对音频的分析，没有发现声响。',
    '这段音频中未捕捉到任何声音。',
    '从音频中没有识别到任何人物或物体的声音。',
    '音频中没有检测到任何声源。',
    '根据音频分析结果，没有发现任何声音。',
    '这段音频里没有听到任何声响。',
    '音频分析显示没有检测到声音。',
    '从音频中未发现任何声源。',
    '这段音频中没有检测到任何人物或物体的声音。',
    '音频分析结果显示未检测到声响。',
    '根据音频，没有发现任何人物或物体发出的声音。',
    '这段音频里没有捕捉到任何声源。',
    '从音频中没有识别到任何声响。',
    '音频分析结果显示没有发现声音。',
    '这段音频中未检测到任何声源。',
    '根据音频分析，没有发现任何声响。',
    '这段音频里没有识别到任何声音。',
    '音频中没有检测到任何声响。',
    '通过分析音频，没有发现任何人物或物体发出的声音。'
]

# Mapping of presence fields to their translated names
presence_fields = {
    # '1-1_small-sounding-engine_presence': '小型发动机声',
    # '1-2_medium-sounding-engine_presence': '中型发动机声',
    # '1-3_large-sounding-engine_presence': '大型发动机声',
    # '1-X_engine-of-uncertain-size_presence': '发动机声',
    # '2-1_rock-drill_presence': '岩钻声',
    # '2-2_jackhammer_presence': '风镐声',
    # '2-3_hoe-ram_presence': '钩锤声',
    # '2-4_pile-driver_presence': '打桩机声',
    # '2-X_other-unknown-impact-machinery_presence': '冲击机械声',
    # '3-1_non-machinery-impact_presence': '非机械撞击声',
    # '4-1_chainsaw_presence': '电锯声',
    # '4-2_small-medium-rotating-saw_presence': '小型中型旋转锯声',
    # '4-3_large-rotating-saw_presence': '大型旋转锯声',
    # '4-X_other-unknown-powered-saw_presence': '动力锯声',
    # '5-1_car-horn_presence': '汽车喇叭声',
    # '5-2_car-alarm_presence': '汽车警报声',
    # '5-3_siren_presence': '警笛声',
    # '5-4_reverse-beeper_presence': '倒车蜂鸣声',
    # '5-X_other-unknown-alert-signal_presence': '警报信号声',
    # '6-1_stationary-music_presence': '固定音乐声',
    # '6-2_mobile-music_presence': '移动音乐声',
    # '6-3_ice-cream-truck_presence': '冰淇淋车音乐声',
    # '6-X_music-from-uncertain-source_presence': '不确定来源的音乐声',
    # '7-1_person-or-small-group-talking_presence': '人或小群体谈话声',
    # '7-2_person-or-small-group-shouting_presence': '人或小群体喊叫声',
    # '7-3_large-crowd_presence': '人群喧哗声',
    # '7-4_amplified-speech_presence': '扩音器讲话声',
    # '7-X_other-unknown-human-voice_presence': '人声',
    # '8-1_dog-barking-whining_presence': '狗叫声',
    # '1-1_small-sounding-engine_proximity': '小型发动机接近声',
    # '1-2_medium-sounding-engine_proximity': '中型发动机接近声',
    # '1-3_large-sounding-engine_proximity': '大型发动机接近声',
    # '1-X_engine-of-uncertain-size_proximity': '发动机接近声',
    # '2-1_rock-drill_proximity': '岩钻接近声',
    # '2-2_jackhammer_proximity': '手提钻接近声',
    # '2-3_hoe-ram_proximity': '钩锤接近声',
    # '2-4_pile-driver_proximity': '打桩机接近声',
    # '2-X_other-unknown-impact-machinery_proximity': '冲击机械接近声',
    # '3-1_non-machinery-impact_proximity': '非机械撞击接近声',
    # '4-1_chainsaw_proximity': '电锯接近声',
    # '4-2_small-medium-rotating-saw_proximity': '小型中型旋转锯接近声',
    # '4-3_large-rotating-saw_proximity': '大型旋转锯接近声',
    # '4-X_other-unknown-powered-saw_proximity': '动力锯接近声',
    # '5-1_car-horn_proximity': '汽车喇叭接近声',
    # '5-2_car-alarm_proximity': '汽车警报接近声',
    # '5-3_siren_proximity': '警笛接近声',
    # '5-4_reverse-beeper_proximity': '倒车蜂鸣接近声',
    # '5-X_other-unknown-alert-signal_proximity': '警报信号接近声',
    # '6-1_stationary-music_proximity': '固定音乐接近声',
    # '6-2_mobile-music_proximity': '移动音乐接近声',
    # '6-3_ice-cream-truck_proximity': '冰淇淋车音乐接近声',
    # '6-X_music-from-uncertain-source_proximity': '不确定来源的音乐接近声',
    # '7-1_person-or-small-group-talking_proximity': '人或小群体谈话接近声',
    # '7-2_person-or-small-group-shouting_proximity': '人或小群体喊叫接近声',
    # '7-3_large-crowd_proximity': '大群体接近声',
    # '7-4_amplified-speech_proximity': '扩音器讲话接近声',
    # '7-X_other-unknown-human-voice_proximity': '人声接近声',
    # '8-1_dog-barking-whining_proximity': '狗叫接近声',
    '1_engine_presence': ['发动机声', '引擎声', '机器引擎声', '发动机运转声'],
    '2_machinery-impact_presence': ['机械撞击声', '机器撞击声', '金属撞击声', '机械冲击声'],
    '3_non-machinery-impact_presence': ['非机械撞击声', '普通撞击声', '非金属撞击声', '物体撞击声'],
    '4_powered-saw_presence': ['动力锯声', '电锯声', '机械锯声', '链锯声'],
    '5_alert-signal_presence': ['警报信号声', '报警声', '警报声', '信号提示音'],
    '6_music_presence': ['音乐声', '音乐播放声', '背景音乐', '旋律声'],
    '7_human-voice_presence': ['人声', '说话声', '人类声音', '讲话声'],
    '8_dog_presence': ['狗叫声', '犬吠声', '狗吠声', '狗叫的声音']
}

exist_sound = ['1', 'near', 'far']


def process_row(row):
  audio_filename = row['audio_filename']
  translated_cv = []
  cnt = 0

  for field, translations in presence_fields.items():
    if row[field] in exist_sound:
      cnt += 1
      # 随机选择一个翻译
      translated_cv.append(random.choice(translations))

  # 构建 GPT 的输出值
  if cnt == 0:
    gpt_value = random.choice(nosound_seeds)
  else:
    gpt_value = random.choice(answer_seeds) + "、".join(translated_cv) + '。'
    if random.random() < 0.6:
      gpt_value = "、".join(translated_cv) + '。'

  # 构建 JSON 对象
  json_object = {
      "audio": f"SONYC/{audio_filename}",
      "conversations": [
          {
              "from": "human",
              "value": random.choice(question_seeds),
              "input_modality": "audio"
          },
          {
              "from": "gpt",
              "value": gpt_value,
              "output_modality": "text"
          }
      ]
  }

  return json_object


def process_csv(csv_file):
  json_data = []

  with open(csv_file, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    with ThreadPoolExecutor(max_workers=4) as executor:
      futures = [executor.submit(process_row, row) for row in reader]
      for future in futures:
        json_data.append(future.result())

  return json_data

# Function to save JSON data to a file


def save_json(json_data, json_file):
  with open(json_file, 'w', encoding='utf-8') as f:
    # json.dump(json_data, f, ensure_ascii=False, indent=4)
    json.dump(json_data, f, ensure_ascii=False, separators=(',', ':'))


if __name__ == "__main__":
  csv_file = 'annotations.csv'  # Replace with your CSV file path
  json_file = 'json/SONYC_ch.json'  # Output JSON file path

  print("Processing CSV file...")
  json_data = process_csv(csv_file)
  print("Saving JSON data...")
  save_json(json_data, json_file)
  print("Process completed.")
