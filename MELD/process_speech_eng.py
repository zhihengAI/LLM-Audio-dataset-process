import csv
import json
import os
import random
import glob
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm  # Import tqdm for progress bar
import chardet


question_seeds = [
    'What did the speaker say in this audio?',
    'What is the speaker saying in the audio?',
    'What can be heard from the audio about what the speaker said?',
    'What did the speaker say in this audio clip?',
    'What content did the speaker express in the audio?',
    'After listening to this audio, can you figure out what the speaker said?',
    'From this audio, what can be inferred about what the speaker is saying?',
    'What exactly is the speaker saying in this audio?',
    'Can you hear what the speaker is saying in the audio?',
    'What content is the speaker expressing in the audio?',
    'Can you hear what the speaker is expressing in this audio?',
    'Can you identify what the speaker is saying from the audio?',
    'What is the speaker saying in this audio?',
    'Can you figure out what the speaker is saying from the audio?',
    'What content is the speaker expressing in the audio?',
    'What is the speaker talking about in this audio?',
    'What is the speaker expressing in the audio?',
    'Can you hear what the speaker is saying from this audio?',
    'What information is the speaker conveying in the audio?',
    'Can you hear what the speaker’s speech content is in this audio?',
    'What exactly is the speaker saying in the audio?',
    'What did the speaker say in this audio clip?',
    'Can you figure out what the speaker is saying from this audio?',
    'What is the speaker’s speech content in this audio?',
    'Can you figure out what the speaker is saying from this audio?'
]


answer_seeds = [
    'From the audio, it can be heard that the speaker is saying ',
    'From the audio, it can be inferred that the speaker is saying ',
    'It can be heard from the audio that the speaker is saying ',
    'From the content of the audio, it’s clear that the speaker is saying ',
    'The audio reveals that the speaker is saying ',
    'From the audio, it can be known that the speaker is saying ',
    'The audio confirms that the speaker is saying ',
    'The audio clearly shows that the speaker is saying ',
    'From listening to the audio, it can be inferred that the speaker is saying ',
    'From the content of the audio, it can be heard that the speaker is saying ',
    'The recording reveals that the speaker is saying ',
    'The audio indicates that the speaker is saying ',
    'The content of the audio reveals that the speaker is saying ',
    'The audio identifies that the speaker is saying ',
    'The voice in the audio indicates that the speaker is saying ',
    'The audio clearly reveals that the speaker is saying ',
    'The audio suggests that the speaker is saying ',
    'The audio directly indicates that the speaker is saying ',
    'The dialogue in the audio suggests that the speaker is saying ',
    'The audio fully reveals that the speaker is saying '
]


def read_csv_annotations(csv_file):
  annotations = []
  with open(csv_file, mode='rb') as csvfile:
    result = chardet.detect(csvfile.read())
    csvencoding = result['encoding']
    print('Encoding detected: ', csvencoding)

  with open(csv_file, newline='', encoding=csvencoding) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      annotations.append(row)
  return annotations


def process_audio_file(file_path, annotation, base_dir):
  # Get the file name (without path)
  fname = os.path.basename(file_path)
  # Get the utterance and randomly choose a seed
  utterance = annotation['Utterance']

  answer_seed = random.choice(answer_seeds)
  if random.random() < 0.6:
    answer_seed = ''

  # Construct JSON data
  json_data = {
      "audio": f"MELD/{base_dir}/{fname}",
      "conversations": [
          {
              "from": "human",
              # Ignore question_seeds here, directly give an example
              "value": random.choice(question_seeds),
              "input_modality": "audio"
          },
          {
              "from": "gpt",
              "value": f'{answer_seed}\"{utterance}\".',
              "output_modality": "text"
          }
      ]
  }

  return json_data

# Process a .csv file and corresponding .wav folder, and append results to the results list


def process_csv_and_wav(csv_file, wav_folder, results):
  # Determine if it is train or dev
  base_dir = "train" if "train" in csv_file else "dev"

  # Read the CSV file
  annotations = read_csv_annotations(csv_file)

  # Get all .wav files and sort them
  wav_files = sorted(glob.glob(os.path.join(wav_folder, '*.wav')))

  # Check the number of annotations and .wav files, and trim them to the same length
  min_length = min(len(annotations), len(wav_files))
  annotations = annotations[:min_length]
  wav_files = wav_files[:min_length]

  # Use ThreadPoolExecutor for multithreading, with progress bar
  with ThreadPoolExecutor(max_workers=8) as executor:
    future_to_file = {executor.submit(
        process_audio_file, file_path, annotations[i], base_dir): file_path for i, file_path in enumerate(wav_files)}
    for future in tqdm(future_to_file, desc=f"Processing {wav_folder}", total=len(future_to_file)):
      result = future.result()
      results.append(result)

  print(f"All files in {wav_folder} processed.")

# Main function to process multiple .csv and .wav folders, and merge results into a JSON file


def main(csv_files, wav_folders, output_json_file):
  results = []

  for csv_file, wav_folder in zip(csv_files, wav_folders):
    process_csv_and_wav(csv_file, wav_folder, results)

  # Save all results to a JSON file
  with open(output_json_file, 'w', encoding='utf-8') as json_file:
    # json.dump(results, json_file, ensure_ascii=False, indent=4)
    json.dump(results, json_file, ensure_ascii=False, separators=(',', ':'))

  print(f"All data saved to {output_json_file}")


if __name__ == "__main__":
  # csv_files = ["dev_sent_emo.csv", "train_sent_emo.csv"]  # Replace with your CSV file path list
  # wav_folders = ["dev_wav", "train_wav"]    # Replace with your .wav folder path list
  csv_files = ["train_sent_emo.csv"]
  wav_folders = ["train_wav"]
  output_json_file = "json/MELD_speech_eng.json"  # Merged JSON file name
  main(csv_files, wav_folders, output_json_file)
