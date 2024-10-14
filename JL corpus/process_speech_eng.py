import os
import json
import random
import threading

question_seeds = [
    "What did the speaker say in this audio?",
    "What is the speaker saying in the audio?",
    "What can be heard from the audio that the speaker said?",
    "What content did the speaker say in this audio?",
    "What is the speaker expressing in the audio?",
    "After listening to this audio, can you tell what the speaker said?",
    "From this audio, what can be inferred that the speaker said?",
    "What is the specific content the speaker said in this audio?",
    "Can you hear what the speaker said in the audio?",
    "What content did the speaker express in the audio?",
    "Can you tell what the speaker is expressing in this audio?",
    "Can you identify what the speaker said in the audio?",
    "What is the speaker saying in this audio?",
    "From the sound in the audio, can you know what the speaker said?",
    "What is the speaker expressing in the audio?",
    "What is the speaker's speech content in this audio?",
    "What is the speaker expressing in the audio?",
    "Can you tell what the speaker said from this audio?",
    "What information did the speaker convey in the audio?",
    "Can you hear the speaker's speech content in this audio?",
    "What exactly did the speaker say in the audio?",
    "What did the speaker say in this audio?",
    "Can you tell what the speaker said from this audio?",
    "What is the speaker's speech content in this audio?",
    "Can you tell what the speaker is saying from this audio?",
]

answer_seeds = [
    "It can be heard from the audio that",
    "It can be inferred from the audio that",
    "It can be heard from the audio that ",
    "It is clearly evident from the content of the audio that",
    "It can be heard from the audio that ",
    "It can be known from the audio that",
    "It can be determined from the audio that",
    "It is clearly indicated from the audio that",
    "It can be heard from the audio that ",
    "It can be heard from the content of the audio that",
    "It can be heard from the recording that",
    "It can be heard from the audio that",
    "It can be heard from the tone of the audio that",
    "It can be heard from the content of the audio that",
    "It can be identified from the audio that",
    "It can be heard from the sound of the audio that",
    "It is clearly evident from the audio that",
    "It can be distinguished from the audio that",
    "It can be directly known from the audio that",
    "It can be heard from the conversation in the audio that",
    "It can be fully heard from the audio that"
]

# Get all .txt files in the folder


def get_txt_files(folder):
  return [f for f in os.listdir(folder) if f.endswith('.txt')]

# Processing logic to answer what was said


def process_file(txt_file, folder, results):
  # Extract information from the filename
  base_name = os.path.splitext(txt_file)[0]
  parts = base_name.split('_')
  gender = parts[0] if len(parts) > 0 else ''

  # Read .txt file content
  with open(os.path.join(folder, txt_file), 'r') as f:
    text_content = f.read().strip()

  # Determine pronoun based on gender
  pronoun = "she" if "female" in gender else "he"

  if random.random() < 0.6:
    answer_seed = f'\"{text_content}\".'
  else:
    answer_seed = f'{random.choice(answer_seeds)} {pronoun} said \"{text_content}\".'

  # Construct a single JSON item
  json_data = {
      "audio": f"JLcorpus/{base_name}.wav",
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

  results.append(json_data)


def process_files_multithreaded(folder, output_file, num_threads=8):
  txt_files = get_txt_files(folder)
  results = []
  threads = []

  for txt_file in txt_files:
    thread = threading.Thread(
        target=process_file, args=(txt_file, folder, results))
    threads.append(thread)
    thread.start()

    # Control the number of threads
    if len(threads) >= num_threads:
      for t in threads:
        t.join()
      threads = []

  # Wait for remaining threads to finish
  for t in threads:
    t.join()

  # Write all data to the JSON file at once
  with open(output_file, 'w', encoding='utf-8') as json_out:
    # json.dump(results, json_out, ensure_ascii=False, indent=4)
    json.dump(results, json_out, ensure_ascii=False, separators=(',', ':'))

  print(f"All data has been written to {output_file}")


# Main function
if __name__ == "__main__":
  # Replace with your folder path
  folder = "Raw JL corpus (unchecked and unannotated)/JL(wav+txt)/"
  # Replace with the output JSON file path
  output_file = "json/JLcorpus_speech_eng.json"

  process_files_multithreaded(folder, output_file, num_threads=8)
