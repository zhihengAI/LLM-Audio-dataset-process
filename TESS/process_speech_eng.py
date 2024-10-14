import os
import json
import random
from concurrent.futures import ThreadPoolExecutor

question_seeds = [
    'What did the speaker say in this audio?',
    'What is the speaker saying in the audio?',
    'What can you hear the speaker saying in the audio?',
    'What content did the speaker express in this audio?',
    'What message is the speaker conveying in the audio?',
    'After listening to this audio, can you tell what the speaker said?',
    'From this audio, what can you determine the speaker is saying?',
    'What exactly is the speaker saying in this audio?',
    'Can you hear what the speaker is saying in the audio?',
    'What content is the speaker expressing in the audio?',
    'Can you tell what the speaker is conveying in this audio?',
    'Can you distinguish what the speaker said in the audio?',
    'What is the speaker talking about in this audio?',
    'Can you figure out what the speaker is saying from the audio?',
    'What content is the speaker conveying in the audio?',
    'What did the speaker mention in this audio?',
    'What is the speaker expressing in the audio?',
    'Can you identify what the speaker said from this audio?',
    'What message is the speaker delivering in the audio?',
    'Can you hear what the speaker is talking about in this audio?',
    'What exactly did the speaker say in the audio?',
    'What did the speaker mention in this audio?',
    'Can you tell what the speaker is saying from this audio?',
    'What did the speaker talk about in this audio?',
    'Can you hear what the speaker is saying in this audio?',
]

answer_seeds = [
    'You can hear from the audio that',
    'The audio indicates that',
    'It is clear from the audio that',
    'The audio content clearly shows that',
    'You can hear in the audio that',
    'The audio suggests that',
    'The audio confirms that',
    'The audio clearly indicates that',
    'You can tell from the audio that',
    'The content in the audio reveals that',
    'You can hear from the recording that',
    'You can tell from the audio that',
    'The tone in the audio suggests that',
    'The audio content suggests that',
    'You can identify from the audio that',
    'The audio sound reveals that',
    'It is obvious from the audio that',
    'You can distinguish from the audio that',
    'The audio directly shows that',
    'The conversation in the audio reveals that',
    'You can fully hear in the audio that'
]


def process_audio_file(parent_folder_name, audio_name):
  audio_key = audio_name.split('_')[1].replace(".wav", "")

  if random.random() < 0.6:
    answer_seed = f'\"say the word {audio_key}.\"'
  else:
    answer_seed = f'{random.choice(answer_seeds)} she is saying \"say the word {audio_key}.\".'

  # Generate JSON structure
  json_data = {
      "audio": f"TESS/{parent_folder_name}/{audio_name}",
      "conversations": [
          {
              "from": "human",
              "value": random.choice(question_seeds),
              "input_modality": "audio"
          },
          {
              "from": "gpt",
              "value": f'{answer_seed}',
              "output_modality": "text"
          }
      ]
  }

  return json_data


def process_folder(root_dir):
  json_results = []

  with ThreadPoolExecutor(max_workers=8) as executor:
    futures = []
    for parent_folder_name in os.listdir(root_dir):
      parent_folder_path = os.path.join(root_dir, parent_folder_name)
      if os.path.isdir(parent_folder_path):
        for audio_name in os.listdir(parent_folder_path):
          if audio_name.endswith('.wav'):
            future = executor.submit(
                process_audio_file, parent_folder_name, audio_name)
            futures.append(future)

    for future in futures:
      result = future.result()
      json_results.append(result)

  # Save the results to a JSON file
  with open('json/TESS_speech_eng.json', 'w', encoding='utf-8') as f:
    # json.dump(json_results, f, ensure_ascii=False, indent=4)
    json.dump(json_results, f, ensure_ascii=False, separators=(',', ':'))

  print("All files processed and saved to json.")


if __name__ == "__main__":
  root_dir = "TESS"
  process_folder(root_dir)
