import os
import json
import random
from concurrent.futures import ThreadPoolExecutor

# 假设的问答种子
question_seeds = [
    '这段音频的场景是在什么地方？',
    '这个音频是在什么场景录制的？',
    '这段录音中的背景声音让人联想到什么样的环境或场所？',
    '分析音频中的声音线索，你能推测出这是在哪里？',
    '你能否根据音频里的声音特征，猜测音频环境是在什么地方？',
    '音频中出现的背景音以及其它线索音是否能指示这是在哪里？',
    '这段音频的音效会出现在什么样的场景？',
    '音频中的环境音效能让你想到什么地方？',
    '你能根据音频中的声音元素推测出这是在哪个地点录制的吗？',
    '听完这段音频，你觉得音频发生场所在什么样的环境中？',
    '从音频中的声音细节出发，你能猜测这段音频是在什么场景下录制的吗？',
    '音频中出现的声音特征能否帮助你定位录音的具体场所？',
    '音频中的声音效果能否让你联想到某个特定的场景？',
    '结合音频中的声音特征，你能推测这段音频是在什么地方录制的吗？',
    '通过分析音频中的声音线索，你觉得这段录音的地点可能是哪里？',
    '从音频中的背景声分析，你能猜测出录音的环境是什么样的吗？',
    '你觉得这段音频的录音地点具体是哪一种场所？',
    '音频中的特定声音和背景音能帮助你推测这段录音的场景吗？',
    '你能否根据音频中的回声和混响判断出音频的环境是在什么地方？',
    '音频中捕捉到的声音元素让你联想到什么样的环境或场所？',
    '听完音频后，你能推断出录音的具体场景吗？',
    '从音频中出现的声音线索来看，你觉得这段录音的场景是什么样的？',
    '结合音频中的背景声音，你能推测出录音的场所吗？',
    '通过分析音频中的特定声音线索，你觉得这段录音的场景可能是在哪里？',
    '你能否根据音频中的音效内容和背景音，推测出录音的具体场所？',
    '音频中的各种声音特征能指明这段录音的环境是在什么地方吗？',
    '从音频中的环境音和背景声来看，你觉得这段录音是在什么样的场所进行的？',
    '结合音频中的各种声音线索，你能推测这段音频的录制地点是什么样的吗？',
    '通过音频中的声音线索和环境音效，你能猜测录音的地点是哪里吗？',
    '根据音频中的声音特征，你能说出这段录音的环境是在什么地方吗？'
]

# 修改后的 answer_seeds
answer_seeds = [
    '根据音频的内容和其中捕捉到的声音特征，这段音频的场景很可能是在',
    '根据音频中的背景音和物体互动音，这段音频的地点可能是在',
    '通过分析音频中的各种声音元素，这段录音很可能是在',
    '从音频中的背景声和环境音效来看，这段音频的录制地点可能是在',
    '鉴于音频中捕捉到的特定声音，这段录音的场景很有可能是在',
    '结合音频中听到的声音特征，这段音频的场景可能是在',
    '通过音频中的环境声音和背景音效，可以推测这段录音是在',
    '音频中的声音线索表明，这段录音很可能是在',
    '从音频中识别出的背景音来看，这段音频的场景可能是在',
    '通过对音频中的声音特征进行分析，可以推断这段录音的地点是在',
    '分析音频中的背景声音，我们可以猜测这段音频是在',
    '从音频中的声效细节来看，这段音频很可能录制于',
    '通过音频中的声音线索，可以推测这段录音的场景是',
    '根据音频捕捉到的背景音效，这段录音的地点可能是在',
    '从音频中的环境音效分析，这段音频的录制场所可能是在',
    '通过音频中的各种声音特征，我们可以推测这段录音的地点是在',
    '从音频的声音内容分析，这段录音很可能是在',
    '结合音频中的背景声音，可以推断这段录音的场景是在',
    '根据音频中的环境音效，这段录音的地点很可能是在',
    '从音频捕捉到的各种声音特征来看，这段录音可能是在',
    '根据音频中的声音细节，我们可以推测录音地点可能是在',
    '通过音频中的环境噪音和其他声音特征，可以推断这段录音是在',
    '音频中的背景音效提示，这段录音的场景很可能是在',
    '从音频中的特定声音元素来看，这段录音的地点可能是在',
    '通过音频捕捉到的声音，可以推测这段录音是在',
    '结合音频中的音效内容，可以推断录音地点是在',
    '根据音频中的声音线索，这段音频的场景可能是在',
    '通过音频中的背景噪音，我们可以猜测这段录音是在',
    '音频中的声音提示，这段录音的场景可能是在',
    '根据音频中的各种声音特征，这段音频的场景很可能是在',
    '通过仔细分析音频中的背景声音和环境音效，可以推测这段录音是在',
    '从音频中的不同声音元素和背景噪音来看，这段录音的地点可能是在',
    '结合音频中的背景音效和物体互动音，可以推测这段音频的录制地点是在',
    '根据音频捕捉到的各种声音特征，这段音频的场景可能是在',
    '通过音频中的环境音效和特定声音元素，可以推测这段录音的场所是在',
    '从音频中的声音特征和背景音效分析，这段录音的地点很可能是在',
    '根据音频内容中的背景噪音和环境声音，我们可以推测这段录音是在',
    '通过音频中的各种声音线索和背景噪音，这段音频的场景可能是在',
    '从音频中捕捉到的背景声音和其他声音特征来看，这段录音的场景可能是在',
    '结合音频中的特定声音和背景音效，可以推断这段录音的地点是在',
    '通过分析音频中的不同声音元素和环境噪音，可以推测这段录音是在',
    '从音频内容中的背景声和环境音效来看，这段录音的场景可能是在'
]

no_answer_seeds = [
    "在一个未知的地方",
    "在某个不明确的场所",
    "在一个难以辨别的环境中",
    "在一个不确定的地点",
    "在一个未能识别的地方",
    "在一个未明确指出的场所",
    "在一个无法确认的环境中",
    "在某个无法辨认的地方",
    "在一个未说明的位置",
    "在一个模糊的地点"
]

# 扩充后的 folder_translation，每个包含多个选项
folder_translation = {
    "Bus": ["公交车上", "公交车内", "公交车附近", "靠近公交车站", "公交车旁边"],
    "Cafe": ["咖啡店内", "咖啡馆里", "咖啡厅中", "靠近咖啡店", "咖啡馆旁边"],
    "Car": ["汽车里", "汽车附近", "车内", "停在车旁", "汽车旁边"],
    "CrowdedIndoor": ["拥挤的室内空间", "拥挤的场所中", "嘈杂的室内", "人多的地方", "繁忙的室内"],
    "Elevator": ["电梯内", "电梯里", "靠近电梯", "电梯门口", "电梯旁边"],
    "Kitchen": ["厨房里", "厨房内", "靠近厨房", "烹饪区域", "厨房旁边"],
    "Park": ["公园里", "公园内", "靠近游乐场", "公园入口处", "公园附近"],
    "ResidentialArea": ["住宅区内", "住宅区里", "居民区附近", "生活区中", "郊区住宅区"],
    "Restaurant": ["餐厅里", "餐厅内", "餐馆中", "餐馆附近", "靠近餐厅"],
    "Restroom": ["洗手间里", "洗手间内", "卫生间中", "洗手间附近", "公共卫生间旁"],
    "Street": ["街道上", "街道边", "在人行道旁", "街角附近", "马路旁边"],
    "Subway": ["地铁上", "地铁内", "靠近地铁站", "地铁站台旁", "地铁附近"],
    "SubwayStation": ["地铁站里", "地铁站内", "靠近地铁站", "地铁站旁边", "地铁站边上"]
}


def process_audio_file(file_path):
  parent_folder = os.path.basename(os.path.dirname(file_path))
  grandparent_folder = os.path.basename(
      os.path.dirname(os.path.dirname(file_path)))
  audio_name = os.path.basename(file_path)

  translated_folder = folder_translation.get(parent_folder, None)
  if translated_folder:
    translated_folder = random.choice(translated_folder)
  else:
    translated_folder = random.choice(no_answer_seeds)

  if random.random() < 0.6:
    answer_seed = ''
  else:
    answer_seed = random.choice(answer_seeds)

  gpt_value = f'{answer_seed}{translated_folder}。'

  json_item = {
      "audio": f"CochlScene/{grandparent_folder}/{parent_folder}/{audio_name}",
      "conversations": [
          {
              "from": "human",
              "value": random.choice(question_seeds),
              "input_modality": "audio"
          },
          {
              "from": "gpt",
              "value": f'{gpt_value}',
              "output_modality": "text"
          }
      ]
  }

  return json_item


def find_audio_files(base_folder):
  audio_files = []
  for root, dirs, files in os.walk(base_folder):
    for file in files:
      if file.endswith('.wav'):
        audio_file_path = os.path.join(root, file)
        audio_files.append(audio_file_path)
  return audio_files


def main():
  base_folder = "./CochlScene"
  audio_files = find_audio_files(base_folder)

  json_results = []

  with ThreadPoolExecutor(max_workers=8) as executor:
    results = executor.map(process_audio_file, audio_files)

    for result in results:
      json_results.append(result)

  output_file = 'json/CochlScene_ch.json'
  with open(output_file, 'w', encoding='utf-8') as json_file:
    json.dump(json_results, json_file,
              ensure_ascii=False, separators=(',', ':'))

  print(f"All JSON data has been saved to {output_file}")


if __name__ == "__main__":
  main()
