import csv
import json
import random
import threading
from concurrent.futures import ThreadPoolExecutor
import sys

question_seeds = [
    'Which characters or objects made sounds in this audio?',
    'What characters or objects are making sounds in the audio?',
    'Can you identify the characters or objects making sounds in this audio?',
    'What characters or objects are present in the audio?',
    'Which characters or objects are producing sounds in this audio?',
    'Based on the audio, can you identify the characters or objects making sounds?',
    'Are there any specific characters or objects making sounds in this audio?',
    'Can you determine which characters or objects are making sounds in this audio?',
    'What are the sounds of characters or objects in this audio?',
    'Which characters or objects are creating sounds in the audio?',
    'Which characters or objects can be heard in this audio?',
    'Can you identify the characters or objects making sounds in the audio?',
    'What characters or objects are making noise in the audio?',
    'Which characters or objects are present in this audio?',
    'Can you distinguish the characters or objects making sounds in the audio?',
    'Which characters or objects made noises in the audio?',
    'Can you identify the characters or objects speaking in the audio?',
    'Which characters or objects made distinctive sounds in the audio?',
    'Which characters or objects can be heard in this audio?',
    'Can you distinguish the characters or objects making sounds in the audio?',
    'What are the characteristics of the characters or objects making sounds in this audio?',
    'Which characters or objects are making noise in the audio?',
    'Can you identify the characters or objects making sounds in the audio?',
    'Which objects and characters are present in this audio?',
    'Can you identify the characters or objects in the audio?',
    'Which characters or objects are making noises in the audio?',
    'Can you distinguish the characters or objects making sounds in the audio?',
    'Which characters or objects are making noise in the audio?',
    'Which characters or objects can be recognized by their sounds in this audio?',
    'Can you identify the characters or objects making sounds in the audio?'
]

answer_seeds = [
    'Based on the characteristics of the human voices and object sounds in the audio, it can be inferred that there are',
    'Analyzing the sound elements in the audio, it can be determined that there are',
    'From the specific sounds in the audio, it can be inferred that there are',
    'Based on the captured sounds in the audio, it can be inferred that there are',
    'Considering the sound characteristics in the audio, it can be determined that there are',
    'From the details of the sounds in the audio, it can be heard that there are',
    'Based on the human voices and object sounds in the audio, it can be inferred that there are',
    'Analyzing the sounds in the audio, it can be determined that there are',
    'From the sound characteristics in the audio, it can be heard that there are',
    'Based on the sound clues in the audio, it can be inferred that there are',
    'Given the sound characteristics in the audio, it can be inferred that there are',
    'Based on the human voices and object sounds in the audio, it can be inferred that there are',
    'Considering the sound elements in the audio, it can be determined that there are',
    'Based on the specific sounds in the audio, it can be inferred that there are',
    'Analyzing the sound details in the audio, it can be determined that there are',
    'From the captured sound characteristics in the audio, it can be inferred that there are',
    'Based on the sound characteristics in the audio, it can be inferred that there are',
    'From the sound clues in the audio, it can be inferred that there are',
    'Analyzing the sounds in the audio, it can be inferred that there are',
    'Based on the background sounds and object sounds in the audio, it can be determined that there are',
    'From the interaction of human voices and objects in the audio, it can be inferred that there are',
    'Considering the sound details in the audio, it can be inferred that there are',
    'Based on the sound content in the audio, it can be inferred that there are',
    'Analyzing the various sound elements in the audio, it can be determined that there are',
    'From the sound characteristics in the audio, it can be inferred that there are',
    'Based on the human voices and object sounds in the audio, it can be inferred that there are',
    'Considering the sound clues in the audio, it can be determined that there are',
    'From the captured sounds in the audio, it can be inferred that there are',
    'Analyzing the sound details in the audio, it can be inferred that there are',
    'Based on the background sounds and interactions in the audio, it can be determined that there are'
]

nosound_seeds = [
    'No characters or objects were detected in this audio.',
    'Based on audio analysis, no significant sounds were found.',
    'No distinct sounds were captured in this audio.',
    'No sounds from characters or objects were identified in the audio.',
    'No sounds were detected in this audio.',
    'No sounds were found through audio analysis.',
    'No sounds from characters or objects were detected in the audio.',
    'No sounds were heard in the audio.',
    'No sound sources were detected in the audio.',
    'No sounds were identified in this audio.',
    'Audio analysis results show no sounds detected.',
    'No sounds were found through audio analysis.',
    'No sounds were captured in this audio.',
    'No sounds from characters or objects were identified in the audio.',
    'No sound sources were detected in the audio.',
    'Audio analysis results show no sounds detected.',
    'No sounds were heard in this audio.',
    'Audio analysis shows no sounds detected.',
    'No sound sources were detected in the audio.',
    'No characters or objects were detected in this audio.',
    'Audio analysis results show no sounds detected.',
    'No sounds from characters or objects were detected in the audio.',
    'No sound sources were captured in this audio.',
    'No sounds were identified in the audio.',
    'Audio analysis results show no sounds detected.',
    'No sound sources were detected in this audio.',
    'No significant sounds were found through audio analysis.',
    'No sounds were identified in this audio.',
    'No sounds were detected in the audio.',
    'No sounds from characters or objects were found through audio analysis.'
]

presence_fields = {
    '1_engine_presence': ['engine sound', 'motor sound', 'machine engine sound', 'engine running sound'],
    '2_machinery-impact_presence': ['machinery impact sound', 'machine impact sound', 'metal impact sound', 'mechanical impact sound'],
    '3_non-machinery-impact_presence': ['non-machinery impact sound', 'regular impact sound', 'non-metal impact sound', 'object impact sound'],
    '4_powered-saw_presence': ['powered saw sound', 'chainsaw sound', 'mechanical saw sound', 'sawing sound'],
    '5_alert-signal_presence': ['alert signal sound', 'alarm sound', 'warning sound', 'signal tone'],
    '6_music_presence': ['music sound', 'music playing sound', 'background music', 'melody sound'],
    '7_human-voice_presence': ['human voice', 'speaking sound', 'human sound', 'talking sound'],
    '8_dog_presence': ['dog barking', 'dog sound', 'dog barking sound', 'barking sound']
}

exist_sound = ['1', 'near', 'far']


def process_row(row):
  audio_filename = row['audio_filename']
  translated_cv = []
  cnt = 0

  for field, translations in presence_fields.items():
    if row[field] in exist_sound:
      cnt += 1
      # Randomly choose a translation
      translated_cv.append(random.choice(translations))

  # Construct GPT output value
  if cnt == 0:
    gpt_value = random.choice(nosound_seeds)
  else:
    gpt_value = random.choice(answer_seeds) + ", ".join(translated_cv) + '.'
    if random.random() < 0.6:
      gpt_value = ", ".join(translated_cv) + '.'

  # Construct JSON object
  json_object = {
      "audio": f"SONYC/{audio_filename}",
      "conversations": [
          {
              "from": "human",
              "value": random.choice(question_seeds),
              "input_modality": "audio"
          },
          {
              "from": "gpt",
              "value": gpt_value,
              "output_modality": "text"
          }
      ]
  }

  return json_object


def process_csv(csv_file):
  json_data = []

  with open(csv_file, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    with ThreadPoolExecutor(max_workers=4) as executor:
      futures = [executor.submit(process_row, row) for row in reader]
      for future in futures:
        json_data.append(future.result())

  return json_data

# Function to save JSON data to a file


def save_json(json_data, json_file):
  with open(json_file, 'w', encoding='utf-8') as f:
    # json.dump(json_data, f, ensure_ascii=False, indent=4)
    json.dump(json_data, f, ensure_ascii=False, separators=(',', ':'))


if __name__ == "__main__":
  csv_file = 'annotations.csv'  # Replace with your CSV file path
  json_file = 'json/SONYC_eng.json'  # Output JSON file path

  print("Processing CSV file...")
  json_data = process_csv(csv_file)
  print("Saving JSON data...")
  save_json(json_data, json_file)
  print("Process completed.")
