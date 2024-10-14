import os
import json
import random
import threading

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


# 获取文件夹中所有的.txt文件
def get_txt_files(folder):
  return [f for f in os.listdir(folder) if f.endswith('.txt')]


# 回答情绪的处理逻辑
def process_file(txt_file, folder, results):
  # 提取文件名中的信息
  base_name = os.path.splitext(txt_file)[0]
  parts = base_name.split('_')
  gender = parts[0] if len(parts) > 0 else ''

  # # 读取.txt文件内容
  with open(os.path.join(folder, txt_file), 'r') as f:
    text_content = f.read().strip()

  # 确定性别对应的代词
  pronoun = ("她" if "female" in gender else "他")

  if random.random() < 0.6:
    answer_seed = f'\"{text_content}\"。'
  else:
    answer_seed = f'{random.choice(answer_seeds)}{pronoun}在说 \"{text_content}\" 这句话。'

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
              "value": f'{answer_seed}',
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
    # json.dump(results, json_out, ensure_ascii=False, indent=4)
    json.dump(results, json_out, ensure_ascii=False, separators=(',', ':'))

  print(f"All data has been written to {output_file}")


# 主函数
if __name__ == "__main__":
  # 替换为你的文件夹路径
  folder = "Raw JL corpus (unchecked and unannotated)/JL(wav+txt)/"
  output_folder = "json/JLcorpus_speech_ch.json"  # 替换为输出JSON文件的路径

  process_files_multithreaded(folder, output_folder, num_threads=8)
