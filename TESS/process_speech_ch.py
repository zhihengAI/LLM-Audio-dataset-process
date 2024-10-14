import os
import json
import random
from concurrent.futures import ThreadPoolExecutor

question_seeds = [
    '这段音频中说话的人说了什么？',
    '音频中的说话者在说什么？',
    '从音频中可以听出说话者说了什么？',
    '这段音频里说话者说了哪些内容？',
    '音频中的说话者表达了什么内容？',
    '听了这段音频后，你能听出说话者说了什么吗？',
    '通过这段音频，判断说话者在说什么？',
    '这段音频中，说话者的具体内容是什么？',
    '音频里能听出说话者说了什么吗？',
    '音频中说话者表达的内容是什么？',
    '这段音频中，能听出说话者在表达什么吗？',
    '从音频中，你能辨别出说话者说了什么内容吗？',
    '这段音频里的说话者在说些什么？',
    '通过音频中的声音，可以知道说话者在说什么吗？',
    '音频中的说话者在表达什么内容？',
    '这段音频中说话者的发言内容是什么？',
    '音频里说话者在表达什么？',
    '通过这段音频，可以听出说话者说了什么内容吗？',
    '音频中的说话者传递了什么样的信息？',
    '这段音频中，能听出说话者的讲话内容吗？',
    '音频里说话者说的具体是什么？',
    '这段音频中说话者说了些什么？',
    '通过这段音频，能听出说话者在说什么吗？',
    '这段音频中说话者的讲话内容是什么？',
    '你能从这段音频中听出说话者在说什么吗？',
]


answer_seeds = [
    '从音频里能听出，说话者',
    '从音频可以判断出，说话人',
    '从音频中可以听出来，说话',
    '从音频的内容中可以明显听出，说话人',
    '从音频中可以听到，说话者',
    '从音频里可以得知，说话人',
    '从音频中可以确定，说话者',
    '从音频中清晰地表明，说话人',
    '从音频听来，可以听出，说话者',
    '从音频的内容中，可以听到说话人',
    '从录音中可以听出，说话者',
    '从音频中可以听出，说话人',
    '从音频的语气中可以听到，说话者',
    '从音频的内容里可以听出，说话人',
    '从音频中可以识别出，说话者',
    '从音频的声音里，可以听到说话人',
    '从音频中可以很明显地听出，说话者',
    '从音频中可以分辨出，说话人',
    '从音频里可以直接得知，说话者',
    '从音频的对话中可以听出，说话者',
    '从音频中可以完整听到，说话人'
]


def process_audio_file(parent_folder_name, audio_name):
  audio_key = audio_name.split('_')[1].replace(".wav", "")

  if random.random() < 0.6:
    answer_seed = f'\"say the word {audio_key}.\"。'
  else:
    answer_seed = f'{random.choice(answer_seeds)}她在说 \"say the word {audio_key}.\" 这句话。'


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
              "value": f'{answer_seed}',
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
  with open('json/TESS_speech_ch.json', 'w', encoding='utf-8') as f:
    # json.dump(json_results, f, ensure_ascii=False, indent=4)
    json.dump(json_results, f, ensure_ascii=False, separators=(',', ':'))

  print("All files processed and saved to json.")


if __name__ == "__main__":
  root_dir = "TESS"
  process_folder(root_dir)
