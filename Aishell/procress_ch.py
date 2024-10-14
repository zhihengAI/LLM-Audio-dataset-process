import os
import json
import hashlib
import random
import concurrent.futures

# 假设txt文件路径和wav文件夹路径已经定义
txt_file_path = 'transcript/aishell_transcript_v0.8.txt'


question_seeds = ["音频里面的人物说了什么？"]

# 处理一行txt文件内容的函数


def process_line(line):
    # 拆分行：假设行是由空格分开的
    parts = line.strip().split(maxsplit=1)
    if len(parts) != 2:
        return None  # 跳过不完整的行

    wav_filename = parts[0]
    transcription = parts[1]

    # 提取路径中间的[6:10]部分
    subfolder = wav_filename[6:11]
    wav_file_path = os.path.join(subfolder, f"{wav_filename}.wav")

    # 构造JSON对象
    json_data = {
        "audio": f"Aishell/{subfolder}/{wav_filename}.wav",
        "conversations": [
            {
                "from": "human",
                "value": random.choice(question_seeds),
                "input_modality": "audio"
            },
            {
                "from": "gpt",
                "value": transcription.replace(' ', ''),
                "output_modality": "text"
            }
        ]
    }
    return json_data

# 处理所有行的主函数，使用多线程


def process_txt_file_multithreaded():
    # 使用set哈希表存储已经处理的wav文件，避免重复
    processed_wav_files = set()

    # 存储最终的JSON数据
    json_results = []
    output_json_file = 'Aishell-1_ch.json'

    with open(txt_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 使用多线程池并发处理
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        # 提交所有任务
        future_to_line = {executor.submit(
            process_line, line): line for line in lines}

        # 处理完成的任务
        for future in concurrent.futures.as_completed(future_to_line):
            result = future.result()
            if result:
                # 计算哈希以判断是否重复
                wav_hash = hashlib.md5(result["audio"].encode()).hexdigest()
                if wav_hash not in processed_wav_files:
                    processed_wav_files.add(wav_hash)
                    json_results.append(result)
                    # print(f"Processed: {result['audio']}")

    # 将结果写入JSON文件
    with open(output_json_file, 'w', encoding='utf-8') as outfile:
        # json.dump(json_results, outfile, ensure_ascii=False, indent=4)
        json.dump(json_results, outfile, ensure_ascii=False, separators=(',', ':'))

    print(f"Processing complete. JSON saved to {output_json_file}")


# 调用主函数
if __name__ == '__main__':
    process_txt_file_multithreaded()
