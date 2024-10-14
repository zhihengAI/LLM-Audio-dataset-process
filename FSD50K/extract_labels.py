import csv

# 初始化一个空的哈希表（set）
labels_set = set()

# 读取CSV文件并提取labels列的数据
with open('FSD50K.metadata/collection/collection_dev.csv', 'r', encoding='utf-8') as file:  # 替换 'your_file.csv' 为你的文件名
  reader = csv.DictReader(file)
  for row in reader:
    labels = row['labels'].split(',')  # 以逗号分割标签
    for label in labels:
      labels_set.add(label.strip())  # 去除可能的空格并添加到哈希表中

# 读取CSV文件并提取labels列的数据
with open('FSD50K.metadata/collection/collection_eval.csv', 'r', encoding='utf-8') as file:  # 替换 'your_file.csv' 为你的文件名
  reader = csv.DictReader(file)
  for row in reader:
    labels = row['labels'].split(',')  # 以逗号分割标签
    for label in labels:
      labels_set.add(label.strip())  # 去除可能的空格并添加到哈希表中

with open('dev.txt', 'w', encoding='utf-8') as f:
  for label in sorted(labels_set):
    f.write(label + '\n')
