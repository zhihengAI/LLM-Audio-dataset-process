import os
import json
import random
from concurrent.futures import ThreadPoolExecutor

question_seeds = [
    '这段音频里面说话的人的语气情绪如何？',
    '音频中的说话者是用什么样的语气情绪在说话？',
    '分析音频中的声音，说话人的语气情绪是怎样的？',
    '从音频中的语气情绪，可以推测出说话者的情绪。',
    '音频中说话人的语气情绪给人什么样的感觉？',
    '听了这段音频后，判断说话者的语气情绪是什么样的。',
    '这段音频中说话者表达了什么情绪？',
    '通过音频中的语气情绪，可以得出说话者的情绪是什么？',
    '音频中的说话者传递了什么样的情绪？',
    '这段音频中，能感受到说话者的情绪吗？',
    '从这段音频中，判断说话者的情绪是什么？',
    '通过音频中的语气情绪，识别说话者的情绪。',
    '这段音频中的说话者情绪如何？',
    '这段音频中说话者的情绪特征是什么？',
    '音频中能听出说话者的情绪吗？',
    '音频中的说话者是用怎样的语气情绪在讲话？',
    '音频里说话者的语气情绪反映了什么样的情绪？',
    '通过这段音频，判断说话者是用什么情绪在表达？',
    '音频中说话者的语气情绪表现了什么情绪？',
    '这段音频中说话者的情绪是什么样的？',
    '音频中的说话者用什么样的情绪在表达？',
    '从音频中可以听出说话者的情绪是怎样的？',
    '通过这段音频，判断说话者的情绪。',
    '音频中，能听出说话者在表达什么情绪吗？',
    '说话者在音频中的情绪如何？'
]


answer_seeds = [
    '听音频可以感受到，说话者',
    '通过音频可以判断出，说话者',
    '从音频里能听出，说话者',
    '从音频可以感觉到，说话者',
    '听这段音频时，可以听出来，说话者',
    '通过这段音频，可以明显听出，说话者',
    '音频中传达出，说话者',
    '从这段录音中可以感受到，说话者',
    '听完音频，可以得出，说话者',
    '音频中清晰地表明，说话者',
    '听这段录音，可以推测出，说话者',
    '从这段音频听来，可以发现，说话者',
    '从音频的声音中，可以察觉到，说话者',
    '通过音频的语调，可以听出，说话者',
    '从音频内容中，可以辨别出，说话者',
    '通过这段音频的声音，可以听出，说话者',
    '从音频的细节中可以感知到，说话者',
    '听完这段音频，你会注意到，说话者',
    '音频中透露出，说话者',
    '从录音中不难听出，说话者',
    '通过音频的语气情绪，可以听出，说话者',
    '这段音频让人感觉到，说话者',
    '听这段音频，可以感觉到，说话者',
    '通过这段录音，可以明确地感知到，说话者',
    '从音频的内容来看，可以听出，说话者',
    '通过音频的表达方式，可以判断出，说话者',
    '从录音中清晰地感受到，说话者',
    '听这段录音时，会发现，说话者',
    '通过音频中的语调变化，可以听出，说话者',
    '从这段音频的语气情绪中，可以感受到，说话者',
]

emotion_map = {
    "angry": ["生气的", "愤怒的", "恼火的", "烦躁的"],
    "disgust": ["厌恶的", "反感的", "恶心的", "憎恶的"],
    "fear": ["害怕的", "恐惧的", "惊恐的", "焦虑的"],
    "happy": ["开心的", "快乐的", "高兴的", "满足的"],
    "neutral": ["平静的", "中立的", "镇定的", "无动于衷的"],
    "pleasant_surprised": ["惊喜的", "愉快的", "惊讶的", "兴奋的"],
    "surprised": ["惊讶的", "震惊的", "惊异的", "吃惊的"],
    "sad": ["悲伤的", "沮丧的", "忧伤的", "忧郁的"],
}


def process_audio_file(parent_folder_name, audio_name):
  # Extract the emotion and key part of the audio name
  emotion_english = parent_folder_name.split('_')[-1]
  audio_key = audio_name.split('_')[1].replace(".wav", "")

  # Randomly choose a Chinese translation from the emotion_map
  emotion_chinese_options = emotion_map.get(
      emotion_english.lower(), ["未知情绪"])
  emotion_chinese = random.choice(emotion_chinese_options)

  answer_seed = f'{random.choice(answer_seeds)}她的语气是'
  if random.random() < 0.6:
    answer_seed = '语气是'

  # 生成JSON结构
  json_data = {
      "audio": f"TESS/{parent_folder_name}/{audio_name}",
      "conversations": [
          {
              "from": "human",
              "value": random.choice(question_seeds),
              "input_modality": "audio"
          },
          {
              "from": "gpt",
              "value": f'{answer_seed}{emotion_chinese}。',
              "output_modality": "text"
          }
      ]
  }

  return json_data


def process_folder(root_dir):
  json_results = []

  with ThreadPoolExecutor(max_workers=8) as executor:
    futures = []
    for parent_folder_name in os.listdir(root_dir):
      parent_folder_path = os.path.join(root_dir, parent_folder_name)
      if os.path.isdir(parent_folder_path):
        for audio_name in os.listdir(parent_folder_path):
          if audio_name.endswith('.wav'):
            future = executor.submit(
                process_audio_file, parent_folder_name, audio_name)
            futures.append(future)

    for future in futures:
      result = future.result()
      json_results.append(result)

  # 将结果保存到一个JSON文件中
  with open('json/TESS_ch.json', 'w', encoding='utf-8') as f:
    # json.dump(json_results, f, ensure_ascii=False, indent=4)
    json.dump(json_results, f, ensure_ascii=False, separators=(',', ':'))

  print("All files processed and saved to audio_data.json.")


if __name__ == "__main__":
  root_dir = "TESS"
  process_folder(root_dir)
