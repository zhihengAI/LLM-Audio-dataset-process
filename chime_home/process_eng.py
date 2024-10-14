import os
import csv
import json
import random
import concurrent.futures

question_seeds = [
    'What sounds are in this audio?',
    'Can you hear what sounds are in this audio?',
    'What sounds are in this audio clip?',
    'What sounds appear in this audio?',
    'Based on the audio, can you identify what sounds are present?',
    'What sounds can you hear in the audio?',
    'What are the sounds in this audio?',
    'Can you determine what sounds are in this audio?',
    'What sounds can be heard in the audio?',
    'What specific sounds are in this audio?',
    'What sounds can you hear in this audio clip?',
    'Can you identify any sounds in this audio?',
    'Can you distinguish what sounds are in this audio?',
    'What sounds occur in this audio?',
    'What sounds are emitted in this audio?',
    'Listening to this audio, what sounds can you hear?',
    'What sounds can be heard in this audio clip?',
    'What identifiable sounds are in this audio?',
    'Can you recognize what sounds are in the audio?',
    'What sounds can be heard in this audio?',
    'What noises are in this audio?',
    'What noises can you hear in this audio?',
    'What sounds are emitted in this audio clip?',
    'What sounds occur in this audio clip?',
    'What noises are present in this audio?',
    'Can you hear the sounds in this audio?',
    'What noises can be heard in this audio?',
    'What features can you identify in this audio?',
    'Can you distinguish any sounds in this audio?'
]

answer_seeds = [
    'Based on the characteristics of human voices and object sounds in the audio, it can be inferred that there is',
    'By analyzing the sound elements in the audio, it can be determined that there is',
    'From the specific sounds in the audio, it can be seen that there is',
    'Based on the captured sounds in the audio, it can be inferred that this audio contains',
    'Considering the sound features in the audio, it can be concluded that this audio involves',
    'From the sound details in the audio, it can be heard that there is',
    'Based on the human voices and object sounds in the audio, it can be inferred that there is',
    'By analyzing the sounds in the audio, it can be determined that there is',
    'From the analysis of sound characteristics in the audio, it can be heard that there is',
    'Based on the sound clues in the audio, it can be inferred that there is',
    'Given the sound characteristics in the audio, it can be inferred that there is',
    'From the human voices and object sounds in the audio, it can be concluded that there is',
    'Considering the sound elements in the audio, it can be determined that there is',
    'Based on the specific sounds in the audio, it can be inferred that there is',
    'By analyzing the sound details in the audio, it can be concluded that this audio contains',
    'From the captured sound characteristics in the audio, it can be seen that there is',
    'Based on the sound features in the audio, it can be inferred that there is',
    'From the sound clues in the audio, it can be determined that there is',
    'By analyzing the sounds in the audio, it can be inferred that there is',
    'Based on the background sounds and object sounds in the audio, it can be concluded that this audio contains',
    'From the human voices and object interaction sounds in the audio, it can be inferred that there is',
    'Considering the sound details in the audio, it can be inferred that there is',
    'Based on the sound content in the audio, it can be inferred that there is',
    'By analyzing various sound elements in the audio, it can be determined that there is',
    'From the analysis of sound characteristics in the audio, it can be inferred that there is',
    'Based on the human voices and object sounds in the audio, it can be inferred that there is',
    'Considering the sound clues in the audio, it can be concluded that there is',
    'From the captured sounds in the audio, it can be seen that there is',
    'By analyzing the sound details in the audio, it can be inferred that there is',
    'Based on the background sounds and interaction sounds in the audio, it can be determined that there is'
]

no_answer_seeds = [
    'No significant sounds were detected in this audio.',
    'This audio does not contain any recognizable sounds.',
    'There is no sound in this audio.',
    'This audio has no detectable sounds.',
    'Analysis shows that there is no sound in this audio.',
    'This audio is silent and contains no sounds.',
    'No sounds were found in this audio recording.',
    'This audio appears to be completely silent.',
    'There are no audible elements in this audio.',
    'No sound events were identified in this audio.',
    'This audio produced no noise.',
    'There are no sounds in this audio.',
    'No sounds can be heard in this audio.',
    'The recording does not contain any sounds.',
    'This audio clip is empty, with no sounds.',
    'No audible signals were detected in this audio.',
    'This audio is silent and contains no sounds.',
    'No acoustic events were found in this audio.',
    'This audio recording is completely silent.',
    'There are no noise elements in this audio.',
    'This audio does not contain any sounds.',
    'This sound does not contain any sounds.',
    'No audio signals were detected in the recording.',
    'This audio recording is silent and contains no sounds.',
    'No acoustic signals were found in this audio.',
    'Sound analysis shows that this audio is silent.',
    'This audio does not contain any sounds.',
    'No identifiable sounds were detected in this audio.',
    'There is no sound in this audio recording.',
    'This audio is silent and no sounds were detected.'
]

translation_dict = {
    'c': ['children speaking', 'the sound of children', 'kids speaking'],
    'm': ['adult male speaking', 'man speaking', 'male adult speaking'],
    'f': ['adult female speaking', 'woman speaking', 'female adult speaking'],
    'v': ['video game/TV sounds', 'sounds from electronic devices'],
    'p': ['percussive sounds', 'sounds of knocking or impact', 'footsteps or impact sounds'],
    'b': ['sounds from household appliances', 'sounds of household devices', 'sounds of appliances'],
    'o': ['some background sounds', 'ambient sounds', 'background noise']
}


def translate_majorityvote(vote):
  translated_elements = [
      random.choice(translation_dict[char])
      for char in vote if char in translation_dict
  ]
  return ', '.join(translated_elements)


def process_csv_file(csv_file):
  majorityvote = ""
  chunkname = ""

  with open(csv_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
      if row[0] == 'majorityvote':
        majorityvote = row[1]
      if row[0] == 'chunkname':
        chunkname = row[1]

  translated_cv = translate_majorityvote(majorityvote)

  if random.random() < 0.6:
    answer_seed = ''
    translated_cv = translated_cv.capitalize()
  else:
    answer_seed = random.choice(answer_seeds) + ' '


  gpt_value = f'{answer_seed}{translated_cv}.'
  if not translated_cv:
    gpt_value = random.choice(no_answer_seeds)

  json_data = {
      "audio": f"chime_home/{chunkname}.16kHz.wav",
      "conversations": [
          {
              "from": "human",
              "value": random.choice(question_seeds),
              "input_modality": "audio"
          },
          {
              "from": "gpt",
              "value": f'{gpt_value}',
              "output_modality": "text"
          }
      ]
  }
  return json_data


def main(folder_path, output_json_path):
  csv_files = [os.path.join(folder_path, file) for file in os.listdir(
      folder_path) if file.endswith('.csv')]
  json_results = []

  # Use multithreading to process the files
  with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
    futures = {executor.submit(process_csv_file, csv_file): csv_file for csv_file in csv_files}
    for future in concurrent.futures.as_completed(futures):
      csv_file = futures[future]
      try:
        json_data = future.result()
        json_results.append(json_data)
        # print(f"Processed {csv_file} successfully.")
      except Exception as exc:
        print(f"Error processing {csv_file}: {exc}")

  with open(output_json_path, 'w', encoding='utf-8') as f:
    # json.dump(json_results, f, ensure_ascii=False, indent=4)
    json.dump(json_results, f, ensure_ascii=False, separators=(',', ':'))


# Run the main function
if __name__ == "__main__":
  folder_path = "chunks"
  main(folder_path, 'json/chime_home_eng.json')
