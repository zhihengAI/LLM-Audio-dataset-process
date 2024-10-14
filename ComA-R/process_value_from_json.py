import json
import random


def processed_data_to_json(raw_data):
  return '[' + '},{'.join(raw_data.split('}\n{')) + ']'


# 从 json 文件中提取 value 字段值（英文），将其翻译成中文并写回 json 文件中
def extract_values_to_txt(file_path, output_file):
  # 从文件中读取JSON数据
  with open(file_path, 'r', encoding='utf-8') as file:
    # json.load 是从文件解析，json.loads 是从字符串解析
    data = json.load(file)
    # raw_data = file.read()
    # data = processed_data_to_json(raw_data)
    # data = json.loads(data)

  # 用于存储提取的值
  extracted_values = []

  # 遍历每个视频项
  for item in data:
    # 遍历每个对话
    for conversation in item['conversations']:
      # 提取"value"字段并添加到列表中
      extracted_values.append(conversation['value'].replace('\n', ''))

  # 将提取的值写入到输出文件中
  with open(output_file, 'w', encoding='utf-8') as file:
    for value in extracted_values:
      file.write(value + "\n")


def split_file_evenly_by_size(file_path, num_splits):
  with open(file_path, 'rb') as file:
    file_content = file.read()

  total_size = len(file_content)
  size_per_split = total_size // num_splits

  start = 0
  for i in range(num_splits):
    end = start + size_per_split
    if i == num_splits - 1:
      # 最后一个文件包含剩余的所有内容
      end = total_size

    with open(f'{file_path}_part{i + 1}.txt', 'wb') as file:
      file.write(file_content[start:end])
      start = end

  print("splited files")


# 合并分割的文件
def merge_files(original_file_path, num_splits, output_file_path):
  with open(output_file_path, 'w', encoding='utf-8') as output_file:
    for i in range(1, num_splits + 1):
      # 遍历每个文件
      part_file_path = f'{original_file_path}_part{i}.en.zh-CN.txt'
      with open(part_file_path, 'r', encoding='utf-8') as part_file:
        output_file.write(part_file.read())

  print(f"merge {num_splits} files successfully")


def restore_order(a_file_path, b_file_path, output_file_path):
  # 从a.txt中读取英文句子
  with open(a_file_path, 'r', encoding='utf-8') as file:
    english_sentences = [line.strip() for line in file.readlines()]

  # 从b.txt中读取所有行
  with open(b_file_path, 'r', encoding='utf-8') as file:
    b_lines = [line.strip() for line in file.readlines()]

  # 将b.txt的内容分成(英文句子, 中文翻译)对
  b_pairs = [(b_lines[i], b_lines[i + 1]) for i in range(0, len(b_lines), 2)]

  # 创建一个映射，用英文句子映射到它的中文翻译
  translation_map = {english: chinese for english, chinese in b_pairs}

  # 根据a.txt中的顺序，重新组织b.txt的内容
  ordered_pairs = [(sentence, translation_map[sentence]) for sentence in english_sentences if
                   sentence in translation_map]

  # 将有序的对写入到输出文件
  with open(output_file_path, 'w', encoding='utf-8') as file:
    for english, chinese in ordered_pairs:
      file.write(english + '\n' + chinese + '\n')


def delete_odd_line(txt_file, output_txt_file):
  # 打开原始文件，并读取所有行
  with open(txt_file, 'r', encoding='UTF-8') as file:
    lines = file.readlines()

  # 保留偶数行
  even_lines = [line for index, line in enumerate(
      lines, start=1) if index % 2 == 0]

  # 将处理后的数据写回文件
  with open(output_txt_file, 'w', encoding='UTF-8') as file:
    file.writelines(even_lines)


def replace_json_values_with_txt(json_file_path, txt_file_path, output_json_file_path):
  # 读取JSON文件
  def read_json_file():
    with open(json_file_path, 'r', encoding='utf-8') as file:
      # return json.load(file)
      raw_data = file.read()
      data = processed_data_to_json(raw_data)
      return json.loads(data)

  # 读取TXT文件，并返回一个包含每行的列表
  def read_txt_file():
    with open(txt_file_path, 'r', encoding='utf-8') as file:
      return [line.strip() for line in file]

  # 将TXT文件中的行替换到JSON中的value字段
  def replace_values(json_data, lines):
    line_index = 0
    for item in json_data:
      # item['image_name'] += '.jpg'
      item['video'] = item['video'].replace('videochatgpt_tune/', '')

      role_idx = 0
      for conversation in item['conversations']:
        a = {}
        if line_index < len(lines):
          a['value'] = lines[line_index]
          if role_idx % 2 == 0:
            conversation['input_modality'] = 'text'
          else:
            conversation['output_modality'] = 'text'

          role_idx = (role_idx + 1) % 2
          line_index += 1
        else:
          break
      if line_index >= len(lines):
        break
    return json_data

  def merge_instruction_input_output(json_data):
    new_json_data = []
    for ins in json_data:
      tmp = {
          'conversation': [
              {
                  'from': 'human',
                  'value': ins.get('system', '') + '\n' + ins['instruction'] + ins['input'],
                  'input_modality': 'text'
              },
              {
                  'from': 'gpt',
                  'value': ins['output'],
                  'output_modality': 'text'
              }
          ]
      }

      new_json_data.append(tmp)

    return new_json_data

  def replace_first_value_only(json_data, lines):
    line_index = 0
    for item in json_data:
      # 添加标志以检查是否已替换过value
      replaced = False
      for conversation in item['conversation']:
        if line_index < len(lines) and not replaced:
          conversation['value'] = lines[line_index]
          line_index += 1
          # 设置标志，表示已替换过value
          replaced = True
        else:
          # 如果已替换过value，跳出当前循环
          break
      if line_index >= len(lines):
        break
    return json_data

  # 将修改后的JSON数据写回到新文件
  def write_json_file(json_data):
    with open(output_json_file_path, 'w', encoding='utf-8') as file:
      json.dump(json_data, file, ensure_ascii=False, indent=4)

  # 执行替换操作
  json_data = read_json_file()
  # lines = read_txt_file()
  # modified_json = replace_values(json_data, lines)
  # modified_json = replace_first_value_only(json_data, lines)
  modified_json = merge_instruction_input_output(json_data)
  write_json_file(modified_json)


def sampling_from_bella_instruction(input_json_file, output_json_file):
  with open(input_json_file, 'r', encoding='utf-8') as file:
    raw_data = file.read()
    json_data = processed_data_to_json(raw_data)
    json_data = json.loads(json_data)

  selected_json_data = random.sample(json_data, 100000)
  new_json_data = []
  for item in selected_json_data:
    cur_conversation = {}
    cur_conversation['conversation'] = []

    tmp = {}
    tmp['from'] = 'Human'
    tmp['value'] = item['instruction'] + item['input']
    tmp['input_modality'] = 'text'
    cur_conversation['conversation'].append(tmp)

    tmp = {}
    tmp['from'] = 'gpt'
    tmp['value'] = item['output']
    tmp['output_modality'] = 'text'
    cur_conversation['conversation'].append(tmp)

    new_json_data.append(cur_conversation)

  with open(output_json_file, 'w', encoding='utf-8') as file:
    json.dump(new_json_data, file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
  # sampling_from_bella_instruction('datafile\\multimodal\\origin\\Belle_open_source_1M.json',
  #                                 'datafile\\multimodal\\origin\\Belle_open_source_100k.json')

  # 提取value
  # origin_json_file = './datafile/multimodal/origin/try.json'
  origin_json_file = 'CompA-R_convert.json'
  extract_json_file = 'CompA-R_convert_eng.txt'
  extract_values_to_txt(origin_json_file, extract_json_file)
  # extract_values_to_txt('datafile\\multimodal\\origin\\train_json\\videochatgpt_tune_.json',
  # 'datafile\\multimodal\\origin\\train_json\\videochatgpt_tune_values.txt')

  # 将其分割为多个文件
  num_splits = 8
  # split_file_evenly_by_size(extract_json_file2, num_splits)

  # 期间将文件翻译成中文......

  # 合并分割的文件
  # extract_json_file_chinese1 = './datafile/videochat-value1-chinese.txt'
  # extract_json_file_chinese2 = './datafile/videochat-value2-chinese.txt'
  # merge_files(extract_json_file, num_splits, extract_json_file_chinese2)

  # 还原顺序
  # restore_order('datafile\\multimodal\\origin\\train_json\\videochatgpt_tune_values.txt',
  #               'datafile\\multimodal\\origin\\train_json\\videochatgpt_tune_values_trans.txt',
  #               'datafile\\multimodal\\origin\\train_json\\videochatgpt_tune_values_trans_order.txt')

  # 删除原英文行
  # delete_odd_line('datafile\\multimodal\\origin\\train_json\\videochatgpt_tune_values_trans_order.txt',
  #                 'datafile\\multimodal\\origin\\train_json\\videochatgpt_tune_values_chinese.txt')

  # replace_json_values_with_txt('datafile\\multimodal\\origin\\train_json\\videochatgpt_tune_.json',
  #                              'datafile\\multimodal\\origin\\train_json\\videochatgpt_tune_values_chinese.txt',
  #                              'datafile\\multimodal\\origin\\train_json\\videochatgpt_tune_chinese.json')
  # replace_json_values_with_txt('datafile\\multimodal\\stage-2\\zy_Agent_taskparse.json',
  #                              '', 'datafile\\zy_Agent_taskparse_modified.json')
