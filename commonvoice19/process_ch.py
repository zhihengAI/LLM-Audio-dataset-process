import pandas as pd
import json
import os
import concurrent.futures
import random
from tqdm import tqdm


question_seeds = ["这段音频说了什么？", "音频里面的人物说了什么？"]


def process_tsv(file_path):
    print(f"Processing {file_path}...")

    # 读取TSV文件
    df = pd.read_csv(file_path, sep='\t')

    # 存储结果的列表
    json_list = []

    # 遍历每一行
    for index, row in tqdm(df.iterrows(), total=df.shape[0], desc=f"Processing {file_path}"):
        audio_file = row['path']
        sentence = row['sentence']

        # 构建JSON对象
        json_obj = {
            "audio": f"commonvoice19/{audio_file}",
            "conversations": [
                {
                    "from": "human",
                    "value": random.choice(question_seeds),
                    "input_modality": "audio"
                },
                {
                    "from": "gpt",
                    "value": sentence,
                    "output_modality": "text"
                }
            ]
        }

        # 添加到结果列表
        json_list.append(json_obj)

    print(f"Finished processing {file_path}")
    return json_list


def process_multiple_tsv(files):
    final_result = []

    # 使用多线程处理文件
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        # 提交所有任务
        future_to_file = {executor.submit(
            process_tsv, file): file for file in files}

        # 收集每个线程的结果
        for future in concurrent.futures.as_completed(future_to_file):
            file = future_to_file[future]
            try:
                result = future.result()
                final_result.extend(result)  # 合并每个文件的结果
            except Exception as e:
                print(f"Error processing {file}: {e}")

    return final_result


def save_to_json(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        #json.dump(data, f, ensure_ascii=False, indent=4)
        json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
    print(f"JSON file saved to {output_file}")

# 主函数，处理多个文件并保存为一个JSON


def main(tsv_files, output_json):
    print("Starting the TSV processing with multithreading...")

    # 处理多个TSV文件
    final_data = process_multiple_tsv(tsv_files)

    print(len(final_data))
    # 保存到JSON文件
    save_to_json(final_data, output_json)
    print("Processing complete.")


if __name__ == "__main__":
    # 假设你有多个tsv文件路径
    tsv_files = ["dev.tsv", "other.tsv", "train.tsv", "validated.tsv", "test.tsv", "invalidated.tsv"]  # 替换成你的文件路径
    output_json = "json/commonvoice19_ch.json"

    main(tsv_files, output_json)
