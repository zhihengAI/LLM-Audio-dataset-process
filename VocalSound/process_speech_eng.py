import json
import random
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

question_seeds = [
    'What is the person doing in this audio?',
    'What is the person in the audio doing?',
    'Can you tell what the person is doing in the audio?',
    'What action is the person performing in this audio?',
    'Based on the audio, can you guess what the person is doing?',
    'What activity is the person engaged in the audio?',
    'What kind of action is the person performing in this audio?',
    'Listening to the audio, can you identify what the person is doing?',
    'What is the person doing in this audio clip?',
    'What is the person in this audio doing?',
    'Can you tell what the person is doing in the audio?',
    'What is the action of the person in this audio?',
    'Listening to the audio, can you determine what the person is doing?',
    'What is the person doing in this audio?',
    'In this audio clip, can you judge what the person is doing?',
    'Can you judge the person\'s action based on the audio?',
    'What is the behavior of the person in the audio?',
    'What is the person doing in this audio clip?',
    'Can you tell what activity the person is performing in this audio?',
    'What is the behavior of the person in the audio?',
    'What activity is the person engaged in the audio?',
    'Listening to the audio, can you identify the behavior of the person?',
    'What is the person doing in the audio?',
    'What is the person doing in the audio clip?',
    'What is the person\'s action in this audio?',
    'Listening to the audio, can you infer what the person is doing?',
    'What is the person\'s behavior in the audio?',
    'What is the person in the audio doing?'
]

answer_seeds = [
    'Based on the sound characteristics in the audio, it can be inferred that the person is',
    'By analyzing the sounds in the audio, it can be judged that the person is',
    'From the sounds in the audio, it can be heard that the person is',
    'Based on the captured sounds in the audio, it can be inferred that the person is',
    'Considering the details of the sounds in the audio, it can be judged that the person is',
    'Analyzing the sound characteristics in the audio, it can be heard that the person is',
    'Based on the sounds in the audio, it can be inferred that the person is',
    'By analyzing the sounds in the audio, it can be judged that the person is',
    'From the details of the sounds in the audio, it can be heard that the person is',
    'Based on the sound clues in the audio, it can be inferred that the person is',
    'Given the sound characteristics in the audio, it can be inferred that the person is',
    'From the sounds in the audio, the person is',
    'Considering the sound elements in the audio, it can be judged that the person is',
    'Based on the sounds in the audio, it can be inferred that the person is',
    'By analyzing the sound details in the audio, it can be judged that the person is',
    'From the captured sounds in the audio, the person may be',
    'Based on the sound characteristics in the audio, it can be inferred that the person is',
    'From the sound clues in the audio, the person is',
    'By analyzing the sounds in the audio, it can be inferred that the person is',
    'Listening to the sounds in the audio, the person is',
    'Considering the sound details in the audio, it can be inferred that the person is',
    'Based on the sound content in the audio, it can be inferred that the person is',
    'By analyzing various behavioral sound elements in the audio, it can be judged that the person is',
    'Analyzing the sound characteristics in the audio, it can be inferred that the person is',
    'Based on the sounds in the audio, it can be inferred that the person is',
    'Considering the sound clues in the audio, it can be judged that the person is',
    'From the captured sounds in the audio, the person may be',
    'By analyzing the sound details in the audio, it can be inferred that the person is',
    'Based on the analysis of the audio, it can be judged that the person is',
]

# Define translation dictionary
labels_translation = {
    "/m/01j3sz": ["laughing", "smiling", "giggling"],
    "/m/07plz5l": ["sighing", "exhaling", "breathing out"],
    "/m/01b_21": ["coughing", "dry coughing"],
    "/m/0dl9sf8": ["clearing their throat", "throat clearing", "clearing their voice"],
    "/m/01hsr_": ["sneezing"],
    "/m/07ppn3j": ["sniffing", "breathing in", "inhaling"]
}


# Read and process JSON files


def process_json_file(file_path):
  with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

  processed_data = []

  for item in data['data']:
    # Extract the filename
    wav_filename = os.path.basename(item['wav'])
    audio_path = f"VocalSound/{wav_filename}"
    translated_labels = random.choice(labels_translation[item['labels']])

    if random.random() < 0.6:
      answer_seed = ''
      translated_labels = translated_labels.capitalize()
    else:
      answer_seed = random.choice(answer_seeds) + ' '

    conversation = {
        "audio": audio_path,
        "conversations": [
            {
                "from": "human",
                "value": random.choice(question_seeds),
                "input_modality": "audio"
            },
            {
                "from": "gpt",
                "value": f'{answer_seed}{translated_labels}.',
                "output_modality": "text"
            }
        ]
    }

    processed_data.append(conversation)

  return processed_data

# Process files in parallel and merge results


def process_files_in_parallel(file_paths):
  all_processed_data = []
  with ThreadPoolExecutor(max_workers=8) as executor:
    futures = [executor.submit(process_json_file, file_path)
               for file_path in file_paths]
    for future in as_completed(futures):
      try:
        result = future.result()
        all_processed_data.extend(result)
      except Exception as e:
        print(f"Error processing file: {e}")

  # Save all results into a single merged JSON file
  output_file = "json/vocalsound_speech_eng.json"
  with open(output_file, 'w') as f:
    json.dump(all_processed_data, f, ensure_ascii=False, indent=4)
    # json.dump(all_processed_data, f, ensure_ascii=False, separators=(',', ':'))

  print(f"All files processed and merged into {output_file}")


if __name__ == '__main__':
  # Assume there's a set of JSON file paths
  json_files = ["datafiles/tr.json", "datafiles/val.json"]
  process_files_in_parallel(json_files)
