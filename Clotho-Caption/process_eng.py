import csv
import json
import random
import glob
import os

question_seeds = [
    'Analyze the content of this audio.',
    'Describe this audio in detail.',
    'Describe this audio.',
    'Explain this audio.',
    'Interpret the content of this audio.',
    'Tell me the specific content of this audio.',
    'Help me understand the content of this audio.',
    'What is the main content of this audio?',
    'Explain the content of this audio in detail.',
    'Describe the content of this audio specifically.',
    'Analyze this audio.',
    'Explain the content of this audio thoroughly.',
    'Interpret the details of this audio.',
    'Describe the main information of this audio in detail.',
    'What is the content of this audio? Describe it in detail.',
    'Please analyze this audio thoroughly.',
    'Help me explain the detailed content of this audio.',
    'What is the detailed content of this audio?',
    'Interpret this audio in detail.',
    'Tell me the specific content of this audio.',
    'What is the specific content of this audio? Describe it.',
    'Please analyze the information in this audio thoroughly.',
    'Specifically explain the content of this audio.',
    'Describe in detail what this audio is about.',
    'Interpret the specific content of this audio.',
    'Analyze this audio thoroughly.',
    'Describe every detail of this audio in detail.',
    'Please explain the content of this audio thoroughly.',
    'Can you describe this audio in detail?',
    'Specifically analyze the content of this audio.',
    'Explain every detail of this audio thoroughly.',
    'Please describe all the content of this audio.',
    'Help me analyze the content of this audio.',
    'Thoroughly explain all the information in this audio.',
    'Please describe this audio in detail.',
    'Specifically describe the details of this audio.',
    'Thoroughly explain the content of this audio.'
]


def csv_to_json(input_csv_filepaths, output_json_file):
  json_data = []

  for input_csv_filepath in input_csv_filepaths:
    with open(input_csv_filepath, 'r', newline='', encoding='utf-8') as csvfile:
      csvreader = csv.reader(csvfile)
      rows = list(csvreader)

      for idx, row in enumerate(rows):
        for caption in row[1:]:
          # Check if the caption ends with a period, if not, add one
          if not caption.endswith('.'):
            caption += '.'

          tmp = {
              'audio': f'clothocaption/{row[0]}',
              'conversations': [
                  {
                      'from': 'human',
                      'value': random.choice(question_seeds),
                      'input_modality': 'audio'
                  },
                  {
                      'from': 'gpt',
                      'value': caption,
                      'output_modality': 'text'
                  }
              ]
          }

          json_data.append(tmp)

  with open(output_json_file, 'w', encoding='utf-8') as f:
    json.dump(json_data, f, ensure_ascii=False, separators=(',', ':'))


if __name__ == '__main__':
  # Get all CSV files to be processed
  input_csv_filepaths = glob.glob('csvfiles/eng/*.csv')

  # Output JSON file
  output_json_file = 'json/clothocaption_eng.json'
  csv_to_json(input_csv_filepaths, output_json_file)
