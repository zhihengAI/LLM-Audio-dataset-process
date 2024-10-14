import json
from collections import defaultdict
import threading

# 读取json文件函数
def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# 处理一部分数据的函数，将每个部分的数据转换成需要的格式
def process_chunk(data_chunk, result_dict):
    for entry in data_chunk:
        audio_id = entry['audio_id'].split('/')[-1]  # 提取音频文件名
        audio = f"audioset/{audio_id}"
        instruction = entry['instruction']
        output = entry['output']
        
        if audio not in result_dict:
            result_dict[audio] = {'audio': audio, 'conversations': []}
        
        # 判断是否是该音频的第一个对话
        if len(result_dict[audio]['conversations']) == 0:
            result_dict[audio]['conversations'].append({
                'from': 'human',
                'value': instruction,
                'input_modality': 'audio'
            })
        else:
            result_dict[audio]['conversations'].append({
                'from': 'human',
                'value': instruction,
                'input_modality': 'text'
            })
        
        result_dict[audio]['conversations'].append({
            'from': 'gpt',
            'value': output,
            'output_modality': 'text'
        })

# 多线程处理函数
def process_data_multithreaded(data, thread_count=8):
    # 将数据划分成等份
    chunk_size = len(data) // thread_count
    threads = []
    result_dict = defaultdict(dict)  # 结果字典，线程安全
    
    # 启动多个线程处理数据块
    for i in range(thread_count):
        start = i * chunk_size
        end = None if i == thread_count - 1 else (i + 1) * chunk_size
        chunk = data[start:end]
        thread = threading.Thread(target=process_chunk, args=(chunk, result_dict))
        threads.append(thread)
        thread.start()
    
    # 等待所有线程完成
    for thread in threads:
        thread.join()
    
    return result_dict

# 将结果转换成最终json结构
def convert_to_final_format(result_dict):
    return [v for v in result_dict.values()]

# 写入json文件函数
def write_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)
        # json.dump(data, file, ensure_ascii=False, separators=(':', ','))

# 主函数
def main(input_file, output_file):
    # Step 1: 读取输入的JSON文件
    data = read_json(input_file)
    
    # Step 2: 多线程处理数据
    result_dict = process_data_multithreaded(data)
    
    # Step 3: 转换结果为最终格式
    final_data = convert_to_final_format(result_dict)
    
    # Step 4: 写入最终的JSON文件
    write_json(final_data, output_file)

# 示例使用
input_file = 'CompA-R.json'  # 输入json文件路径
output_file = 'CompA-R_convert.json'  # 输出json文件路径
main(input_file, output_file)
