import json
import random
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

question_seeds = [
    '这个音频中的人物在干什么？',
    '音频里的人物在做什么？',
    '你能听出音频中的人物在干什么吗？',
    '这段音频里的人物在进行什么动作？',
    '根据音频，你能猜出人物在做什么吗？',
    '音频中的人物在从事什么行为？',
    '这段音频中，人物在进行什么样的动作？',
    '听音频，你能识别出人物在干什么吗？',
    '音频里的人物正在做什么事情？',
    '这段音频中的人物正在做什么？',
    '音频中能听出人物的行为是什么吗？',
    '这个音频中，人物的动作是什么？',
    '听音频，你能确定人物在做什么吗？',
    '音频中的人物在干啥？',
    '这段音频中，你能判断人物在做什么吗？',
    '你能根据音频判断人物的动作吗？',
    '音频中的人物行为是什么？',
    '这个音频里的人物正在干什么？',
    '这段音频里能听出人物在进行什么行为吗？',
    '音频中人物的行为是什么？',
    '音频中的人物在从事什么活动？',
    '听音频，你能辨别出人物的行为吗？',
    '音频里的人物正在做什么事情？',
    '音频中的人物在干些什么？',
    '这个音频里人物的动作是什么？',
    '听音频，你能推断出人物在做什么吗？',
    '音频中人物的行为动作是什么？',
    '音频里人物在做什么？'
]

answer_seeds = [
    '根据音频中的声音特征，可以推测人物正在',
    '通过分析音频中的声音，可以判断人物在',
    '从音频中的声音来看，人物在',
    '根据音频捕捉到的声音，可以推测人物正在',
    '结合音频中的声音细节，可以判断人物在',
    '从音频中的声音特征分析，可以听出人物在',
    '根据音频中的声音，可以推测人物正在',
    '通过对音频中的声音分析，可以判断人物在',
    '从音频中的声音细节来看，可以听出人物正在',
    '根据音频中的声音线索，可以推断人物正在',
    '鉴于音频中的声音特征，可以推测人物正在',
    '从音频中的声音来看，人物正在',
    '结合音频中的声音元素，可以判断人物在',
    '根据音频中的声音，可以推测人物正在',
    '通过分析音频中的声音细节，可以判断人物在',
    '从音频捕捉到的声音来看，人物可能在',
    '根据音频中的声音特征，可以推断人物正在',
    '从音频中的声音线索来看，人物正在',
    '通过对音频中的声音分析，可以推测人物正在',
    '从音频中的声音来听，人物正在',
    '结合音频中的声音细节，可以推测人物在',
    '根据音频中的声音内容，可以推断人物正在',
    '通过分析音频中的各种行为声音元素，可以判断人物在',
    '从音频中的声音特征分析，可以推测人物正在',
    '根据音频中的声音，可以推断人物正在',
    '结合音频中的声音线索，可以判断人物在',
    '从音频捕捉到的声音来看，人物可能正在',
    '通过分析音频中的声音细节，可以推测人物在',
    '根据分析音频，可以判断人物正在',
]

# 设定翻译字典
labels_translation = {
    "/m/01j3sz": ["发出笑声", "欢笑", "笑", "大笑"],
    "/m/07plz5l": ["叹息", "叹气", "唉声", "呼气"],
    "/m/01b_21": ["咳嗽", "干咳"],
    "/m/0dl9sf8": ["清嗓子", "清嗓", "清喉"],
    "/m/01hsr_": ["打喷嚏"],
    "/m/07ppn3j": ["抽鼻子", "吸气", "用鼻子吸气"]
}


# 读取并解析JSON文件并处理
def process_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    processed_data = []
    
    for item in data['data']:
        # 提取最后的文件名
        wav_filename = os.path.basename(item['wav'])
        audio_path = f"VocalSound/{wav_filename}"
        translated_labels = random.choice(labels_translation[item['labels']])

        answer_seed = random.choice(answer_seeds)
        if random.random() < 0.6:
          answer_seed = ''

        
        conversation = {
            "audio": audio_path,
            "conversations": [
                {
                    "from": "human",
                    "value": random.choice(question_seeds),
                    "input_modality": "audio"
                },
                {
                    "from": "gpt",
                    "value": f'{answer_seed}{translated_labels}。',
                    "output_modality": "text"
                }
            ]
        }
        
        processed_data.append(conversation)
    
    return processed_data

# 多线程处理并合并结果
def process_files_in_parallel(file_paths):
    all_processed_data = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(process_json_file, file_path) for file_path in file_paths]
        for future in as_completed(futures):
            try:
                result = future.result()
                all_processed_data.extend(result)
            except Exception as e:
                print(f"Error processing file: {e}")
    
    # 将所有结果保存到一个合并的JSON文件
    output_file = "json/vocalsound_speech_ch.json"
    with open(output_file, 'w') as f:
        # json.dump(all_processed_data, f, ensure_ascii=False, indent=4)
        json.dump(all_processed_data, f, ensure_ascii=False, separators=(',', ':'))
    
    print(f"All files processed and merged into {output_file}")

if __name__ == '__main__':
  # 假设有一组JSON文件路径
  json_files = ["datafiles/tr.json", "datafiles/val.json"]
  process_files_in_parallel(json_files)
