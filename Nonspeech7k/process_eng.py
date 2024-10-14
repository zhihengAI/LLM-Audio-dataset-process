import os
import csv
import json
import random
import threading
from concurrent.futures import ThreadPoolExecutor

# Number of threads
THREAD_COUNT = 8

# Simulated seeds
question_seeds = [
    'What is the person in this audio doing?',
    'What is the person doing in the audio?',
    'Can you tell what the person in the audio is doing?',
    'What action is the person taking in this audio?',
    'Based on the audio, can you guess what the person is doing?',
    'What activity is the person engaged in the audio?',
    'What kind of action is the person taking in this audio?',
    'Can you identify what the person is doing by listening to the audio?',
    'What is the person doing in the audio?',
    'What is the person in this audio doing?',
    'Can you tell what the person’s behavior is in the audio?',
    'What action is the person taking in this audio?',
    'Can you determine what the person is doing by listening to the audio?',
    'What operation is the person performing in the audio?',
    'What is the person doing in the audio?',
    'Can you tell what the person is doing in this audio?',
    'Can you judge the person’s action based on the audio?',
    'What is the person’s behavior in the audio?',
    'What is the person doing in this audio?',
    'Can you tell what behavior the person is engaged in this audio?',
    'What is the behavior of the person in the audio?',
    'What activity is the person engaged in the audio?',
    'Can you identify the person’s behavior by listening to the audio?',
    'What is the person doing in the audio?',
    'What is the person engaged in the audio?',
    'What is the action of the person in the audio?',
    'Can you infer what the person is doing by listening to the audio?',
    'What is the person’s behavior and actions in the audio?',
    'What is the person doing in the audio?'
]

answer_seeds = [
    'Based on the sound characteristics in the audio, it can be inferred that the person is',
    'By analyzing the sound in the audio, it can be judged that the person is',
    'From the sound in the audio, it can be determined that the person is',
    'Based on the sounds captured in the audio, it can be inferred that the person is',
    'Combining the sound details in the audio, it can be judged that the person is',
    'From the sound characteristics in the audio, it can be heard that the person is',
    'Based on the sound in the audio, it can be inferred that the person is',
    'By analyzing the sound in the audio, it can be judged that the person is',
    'From the sound details in the audio, it can be heard that the person is',
    'Based on the sound clues in the audio, it can be inferred that the person is',
    'Given the sound characteristics in the audio, it can be inferred that the person is',
    'From the sound in the audio, it can be determined that the person is',
    'Combining the sound elements in the audio, it can be judged that the person is',
    'Based on the sound in the audio, it can be inferred that the person is',
    'By analyzing the sound details in the audio, it can be judged that the person is',
    'From the sounds captured in the audio, it can be inferred that the person might be',
    'Based on the sound characteristics in the audio, it can be inferred that the person is',
    'From the sound clues in the audio, it can be determined that the person is',
    'By analyzing the sound in the audio, it can be inferred that the person is',
    'From the sound in the audio, it can be heard that the person is',
    'Combining the sound details in the audio, it can be inferred that the person is',
    'Based on the sound content in the audio, it can be inferred that the person is',
    'By analyzing the various behavioral sound elements in the audio, it can be judged that the person is',
    'From the sound characteristics in the audio, it can be inferred that the person is',
    'Based on the sound in the audio, it can be inferred that the person is',
    'Combining the sound clues in the audio, it can be judged that the person is',
    'From the sounds captured in the audio, it can be inferred that the person might be',
    'By analyzing the sound details in the audio, it can be inferred that the person is',
    'Based on the analysis of the audio, it can be judged that the person is',
]

# Classname translation dictionary
translated_cv = {
    "breath": ["breathing", "gasping", "inhaling", "exhaling"],
    "cough": ["coughing", "light coughing", "dry cough", "dry coughing"],
    "crying": ["crying", "tears", "sobbing", "sniveling"],
    "laugh": ["laughing", "laughing out loud", "giggling"],
    "screaming": ["screaming", "loud screaming", "panic screaming", "high-pitched shouting"],
    "sneeze": ["sneezing", "light sneezing", "repeated sneezing"],
    "yawn": ["yawning", "open-mouth yawning"],
    "yawm": ["yawning", "open-mouth yawning"]
}


def process_csv_file(csv_path, combined_data):
  parent_path_name = "test" if "test" in csv_path else "train"

  with open(csv_path, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)

    for row in reader:
      filename = row["Filename"]
      classname = row["Classname"]

      # Get the translation list, if classname is not in the dictionary, return a list containing the original classname
      translations = translated_cv.get(classname, [classname])
      # Randomly choose a translation from the list
      translated_classname = random.choice(translations)

      answer_seed = f'{random.choice(answer_seeds)} '
      if random.random() < 0.6:
        answer_seed = ''
        translated_classname = translated_classname.capitalize()

      # Build JSON data
      json_data = {
          "audio": f"Nonspeech7k/{parent_path_name}/{filename}",
          "conversations": [
              {
                  "from": "human",
                  "value": random.choice(question_seeds),
                  "input_modality": "audio"
              },
              {
                  "from": "gpt",
                  "value": f'{answer_seed}{translated_classname}.',
                  "output_modality": "text"
              }
          ]
      }

      # Add the constructed data to the combined_data list
      combined_data.append(json_data)


def get_csv_files(directory):
  csv_files = []
  for root, _, files in os.walk(directory):
    for file in files:
      if file.endswith(".csv"):
        csv_files.append(os.path.join(root, file))
  return csv_files

# Main function


def main():
  base_dir = "."
  csv_files = get_csv_files(base_dir)

  combined_data = []

  with ThreadPoolExecutor(max_workers=THREAD_COUNT) as executor:
    futures = []
    for csv_file in csv_files:
      futures.append(executor.submit(
          process_csv_file, csv_file, combined_data))

    # Wait for all threads to complete
    for future in futures:
      future.result()

  # Write all data to a JSON file
  with open("json/Nonspeech7K_eng.json", "w", encoding="utf-8") as outfile:
    # json.dump(combined_data, outfile, ensure_ascii=False, indent=4)
    json.dump(combined_data, outfile,
              ensure_ascii=False, separators=(',', ':'))

  print("All data have been combined")


if __name__ == "__main__":
  main()
