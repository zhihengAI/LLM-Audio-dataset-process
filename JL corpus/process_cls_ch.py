import os
import json
import random
import threading

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


# 情绪的中文翻译
emotion_translations = {
    "happy": ["高兴的", "快乐的", "开心的", "愉快的", "愉悦的"],
    "assertive": ["坚定的", "自信的", "果断的", "坚决的", "坚定自信的"],
    "angry": ["生气的", "愤怒的", "恼怒的", "暴躁的", "气愤的"],
    "apologetic": ["有歉意的", "不好意思的", "愧疚的", "道歉的", "惭愧的"],
    "encouraging": ["鼓舞的", "激励的", "鼓励的", "支持的", "正能量的"],
    "neutral": ["中立的", "冷静的", "平静的", "中性的", "不带感情的"],
    "excited": ["兴奋的", "激动的", "热情的", "欢快的", "亢奋的"],
    "concerned": ["担忧的", "关切的", "挂念的", "焦虑的", "忧心忡忡的"],
    "anxious": ["焦虑的", "不安的", "紧张的", "担心的", "忧虑的"],
    "sad": ["伤心的", "悲伤的", "难过的", "忧伤的", "悲哀的"]
}


# 获取文件夹中所有的.txt文件
def get_txt_files(folder):
  return [f for f in os.listdir(folder) if f.endswith('.txt')]


# 回答情绪的处理逻辑
def process_file(txt_file, folder, results):
  # 提取文件名中的信息
  base_name = os.path.splitext(txt_file)[0]
  parts = base_name.split('_')
  gender = parts[0] if len(parts) > 0 else ''
  emotion = parts[1] if len(parts) > 1 else ''

  # # 读取.txt文件内容
  # with open(os.path.join(folder, txt_file), 'r') as f:
  #   text_content = f.read().strip()

  # 确定性别对应的代词
  pronoun = ("她的" if "female" in gender else "他的") + '语气是'

  # 多样化情感翻译
  emotion_translation = random.choice(
      emotion_translations.get(emotion.lower(), [emotion]))
  
  answer_seed = f'{random.choice(answer_seeds)}{pronoun}'
  if random.random() < 0.6:
    answer_seed = ''
    # answer_seed += f'且是一个{"女性" if "female" in gender else "男性"}在说着 "{text_content}" 这句话。'

  # 构造单个JSON项
  json_data = {
      "audio": f"JLcorpus/{base_name}.wav",
      "conversations": [
          {
              "from": "human",
              "value": random.choice(question_seeds),
              "input_modality": "audio"
          },
          {
              "from": "gpt",
              "value": f'{answer_seed}{emotion_translation}。',
              "output_modality": "text"
          }
      ]
  }

  results.append(json_data)


def process_files_multithreaded(folder, output_file, num_threads=8):
  txt_files = get_txt_files(folder)
  results = []
  threads = []

  for txt_file in txt_files:
    thread = threading.Thread(
        target=process_file, args=(txt_file, folder, results))
    threads.append(thread)
    thread.start()

    # 控制线程数量
    if len(threads) >= num_threads:
      for t in threads:
        t.join()
      threads = []

  # 等待剩余线程完成
  for t in threads:
    t.join()

  # 一次性写入JSON文件
  with open(output_file, 'w', encoding='utf-8') as json_out:
    json.dump(results, json_out, ensure_ascii=False, indent=4)
    # json.dump(results, json_out, ensure_ascii=False, separators=(',', ':'))

  print(f"All data has been written to {output_file}")


# 主函数
if __name__ == "__main__":
  # 替换为你的文件夹路径
  folder = "Raw JL corpus (unchecked and unannotated)/JL(wav+txt)/"
  output_folder = "json/JLcorpus_cls_ch.json"  # 替换为输出JSON文件的路径

  process_files_multithreaded(folder, output_folder, num_threads=8)
