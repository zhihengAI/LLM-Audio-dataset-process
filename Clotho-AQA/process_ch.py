import csv
import json


def extract_values():
  # 打开CSV文件
  with open('clotho_aqa_train_ch.csv', 'r', encoding='utf-8', newline='') as csvfile:
    # 创建CSV读取器
    csvreader = csv.reader(csvfile)

    # 打开目标TXT文件
    with open('values.txt', 'w') as txtfile:
      # 迭代CSV中的每一行
      for row in csvreader:
        # 将第二列内容写入TXT文件
        txtfile.write(row[2] + '\n')


def replace_csv_column_with_txt(input_csv_filepath, txt_filepath, output_csv_filepath, column_index=1):
  # 读取TXT文件内容
  with open(txt_filepath, 'r', encoding='utf-8') as txtfile:
    txt_lines = txtfile.readlines()

  # 打开输入的CSV文件进行读取
  with open(input_csv_filepath, 'r', newline='', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile)
    rows = list(csvreader)

  # 替换CSV文件的指定列内容
  for i, line in enumerate(txt_lines):
    if i < len(rows):
      rows[i][column_index] = line.strip()

  # 将修改后的内容写入到新的CSV文件
  with open(output_csv_filepath, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerows(rows)


def csv_to_json(input_csv_filepath, output_json_file):
  json_data = []
  with open(input_csv_filepath, 'r', newline='', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile)
    rows = list(csvreader)

    for row in rows:
      tmp = {
          'audio': f'clothoaqa/{row[0]}',
          'conversations': [
            {
                'from': 'human',
                'value': row[1],
                'input_modality': 'audio'
            },
              {
                'from': 'gpt',
                'value': f'{row[2]}。',
                'output_modality': 'text'
            }
          ]
      }

      json_data.append(tmp)
  
  with open(output_json_file, 'w', encoding='utf-8') as f:
    json.dump(json_data, f, ensure_ascii=False, separators=(',', ':'))


# extract_values()
# replace_csv_column_with_txt('output.csv',
#                             'values_chinese_answer.txt', 'output.csv', 2)
csv_to_json('clotho_aqa_train_ch.csv', 'json/clothoaqa_ch.json')
