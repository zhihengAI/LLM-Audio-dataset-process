import csv
import json
import os
import random
import glob
from concurrent.futures import ThreadPoolExecutor
import chardet
from tqdm import tqdm  # Import tqdm for progress bar

question_seeds = [
    'What is the tone and emotion of the speaker in this audio?',
    'What kind of tone and emotion is the speaker using in the audio?',
    'Analyze the audio, how is the tone and emotion of the speaker?',
    'From the tone and emotion in the audio, what can be inferred about the speaker’s emotion?',
    'What kind of feeling does the speaker’s tone and emotion in the audio give?',
    'After listening to this audio, what can be judged about the speaker’s tone and emotion?',
    'What emotion does the speaker express in this audio?',
    'From the tone and emotion in the audio, what can be concluded about the speaker’s emotion?',
    'What kind of emotion does the speaker convey in the audio?',
    'Can the speaker’s emotion be felt from this audio?',
    'From this audio, what is the speaker’s emotion?',
    'Identify the speaker’s emotion from the tone and emotion in the audio.',
    'How is the speaker’s emotion in this audio?',
    'What are the emotional characteristics of the speaker in this audio?',
    'Can the speaker’s emotion be heard in the audio?',
    'What kind of tone and emotion is the speaker using in the audio?',
    'What emotion is reflected by the speaker’s tone and emotion in the audio?',
    'From this audio, what emotion is the speaker expressing?',
    'What emotion does the speaker’s tone and emotion convey in the audio?',
    'What is the speaker’s emotion in this audio?',
    'What kind of emotion is the speaker expressing in the audio?',
    'What can be heard about the speaker’s emotion from the audio?',
    'From this audio, what is the speaker’s emotion?',
    'Can the speaker’s emotion be heard in the audio?',
    'What is the speaker’s emotion in the audio?'
]

answer_seeds = [
    'The audio suggests that the speaker\'s emotion is',
    'From the audio, it can be judged that the speaker\'s emotion is',
    'It can be heard from the audio that the speaker\'s emotion is',
    'The audio suggests that the speaker\'s emotion is',
    'Listening to this audio, you can hear that the speaker\'s emotion is',
    'From this audio, it’s obvious that the speaker\'s emotion is',
    'The audio conveys that the speaker\'s emotion is',
    'This recording suggests that the speaker\'s emotion is',
    'After listening to the audio, it can be concluded that the speaker\'s emotion is',
    'The audio clearly indicates that the speaker\'s emotion is',
    'Listening to this recording, it can be inferred that the speaker\'s emotion is',
    'From this audio, it can be found that the speaker\'s emotion is',
    'The voice in the audio suggests that the speaker\'s emotion is',
    'From the tone in the audio, it can be heard that the speaker\'s emotion is',
    'The content of the audio suggests that the speaker\'s emotion is',
    'From the voice in this audio, it can be heard that the speaker\'s emotion is',
    'The details in the audio suggest that the speaker\'s emotion is',
    'After listening to this audio, you will notice that the speaker\'s emotion is',
    'The audio reveals that the speaker\'s emotion is',
    'It’s easy to hear from the recording that the speaker\'s emotion is',
    'The tone and emotion in the audio suggest that the speaker\'s emotion is',
    'This audio suggests that the speaker\'s emotion is',
    'Listening to this audio, you can feel that the speaker\'s emotion is',
    'This recording clearly suggests that the speaker\'s emotion is',
    'From the content of the audio, it can be heard that the speaker\'s emotion is',
    'From the way the audio is expressed, it can be judged that the speaker\'s emotion is',
    'The recording clearly suggests that the speaker\'s emotion is',
    'Listening to this recording, it can be found that the speaker\'s emotion is',
    'The tone changes in the audio suggest that the speaker\'s emotion is',
    'The tone and emotion in this audio suggest that the speaker\'s emotion is',
]

# Dictionary mapping emotions to English translations
emotion_dict = {
    'anger': ['angry', 'mad', 'irritated', 'annoyed'],
    'disgust': ['disgusted', 'repulsed', 'appalled', 'nauseated'],
    'fear': ['fearful', 'scared', 'afraid', 'terrified'],
    'joy': ['happy', 'joyful', 'delighted', 'cheerful'],
    'neutral': ['neutral', 'calm', 'composed', 'unemotional'],
    'sadness': ['sad', 'downhearted', 'melancholic', 'sorrowful'],
    'surprise': ['surprised', 'astonished', 'amazed', 'startled']
}


def read_csv_annotations(csv_file):
  annotations = []
  with open(csv_file, mode='rb') as csvfile:
    result = chardet.detect(csvfile.read())
    csvencoding = result['encoding']
    print('encoding: ', csvencoding)

  with open(csv_file, newline='', encoding=csvencoding) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      annotations.append(row)
  return annotations


def process_audio_file(file_path, annotation, base_dir):
  # Get the file name (without path)
  fname = os.path.basename(file_path)
  # Get emotion and randomly choose an English translation
  emotion = annotation['Emotion']
  translated_emotion = random.choice(emotion_dict[emotion])

  answer_seed = random.choice(answer_seeds)
  if random.random() < 0.6:
    answer_seed = ''
  answer_seed += 'The speaker\'s emotion is'

  # Construct JSON data
  json_data = {
      "audio": f"MELD/{base_dir}/{fname}",
      "conversations": [
          {
              "from": "human",
              # Ignore question_seeds, directly give an example here
              "value": random.choice(question_seeds),
              "input_modality": "audio"
          },
          {
              "from": "gpt",
              "value": f'{answer_seed} {translated_emotion}.',
              "output_modality": "text"
          }
      ]
  }

  return json_data

# Process a .csv file and corresponding .wav folder, and append results to the results list


def process_csv_and_wav(csv_file, wav_folder, results):
  # Determine whether it is train or dev
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
  output_json_file = "json/MELD_emo_eng.json"  # Merged JSON file name
  main(csv_files, wav_folders, output_json_file)
