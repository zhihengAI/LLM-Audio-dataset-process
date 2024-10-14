import os
import json
import random
import concurrent.futures


# 模拟 question_seeds 和 answer_seeds
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


# 性别字典
gender_prefix = {
    "bea": "她的语气情绪是",
    "jenie": "她的语气情绪是",
    "josh": "他的语气情绪是",
    "sam": "他的语气情绪是"
}

# 情绪翻译字典
emotion_translation = {
    "Amused": ["愉快的", "开心的", "有趣的", "被逗乐的", "愉悦的"],
    "Angry": ["愤怒的", "生气的", "暴躁的", "气愤的", "恼怒的"],
    "Disgusted": ["厌烦的", "烦躁的", "恶心的", "不满的", "嫌恶的"],
    "Neutral": ["中性的", "平静的", "冷静的", "平淡的", "不带情感的"],
    "Sleepy": ["困倦的", "困得想睡的", "疲倦的", "昏昏欲睡的", "困得懒洋洋的"]
}


def process_audio_file(parent_folder_name, audio_name):
  # print(f"Processing file: {audio_name} in folder: {parent_folder_name}")

  # 提取情绪关键词
  name_prefix = parent_folder_name.split('_')[0]
  emotion_keyword = parent_folder_name.split('_')[1]
  emotion_chinese = random.choice(
      emotion_translation.get(emotion_keyword, [""]))
  gender_text = gender_prefix.get(name_prefix, [""])

  answer_seed = f'{random.choice(answer_seeds)}{gender_text}'

  if random.random() < 0.6:
    answer_seed = ''

  # 构造 JSON 字典
  json_dict = {
      "audio": f"EmoV_DB/{parent_folder_name}/{audio_name}",
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

  return json_dict


def process_all_files(directory):
  json_data = []

  # 使用8个线程
  with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
    futures = []

    # 遍历目录和文件
    for parent_folder_name in os.listdir(directory):
      parent_folder_path = os.path.join(directory, parent_folder_name)
      if os.path.isdir(parent_folder_path):
        for audio_name in os.listdir(parent_folder_path):
          if audio_name.endswith('.wav'):
            # 提交任务到线程池
            futures.append(
                executor.submit(process_audio_file,
                                parent_folder_name, audio_name)
            )

    # 获取处理结果
    for future in concurrent.futures.as_completed(futures):
      json_data.append(future.result())

  return json_data


# 主函数
if __name__ == "__main__":
  directory = "EmoV_DB"  # 替换为实际的文件夹路径
  result = process_all_files(directory)

  # 将结果保存为 JSON 文件
  with open("json/EmoV_DB_ch.json", "w", encoding="utf-8") as f:
    # json.dump(result, f, ensure_ascii=False, indent=4)
    json.dump(result, f, ensure_ascii=False, separators=(',', ':'))

  print("Processing complete. JSON file saved as output.json")
