import json
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

# Question seeds
question_seeds = [
    "What instrument is playing in this audio?",
    "Which instrument is being played in the audio?",
    "What is this sound from?",
    "Can you hear what instrument is playing in this audio?",
    "Which instrument is being played in this audio?",
    "What instrument is this sound coming from?",
    "Is there an instrument playing in this audio?",
    "What instrument is in this audio?",
    "Can you identify the instrument in this audio?",
    "What instrument is this sound from?",
    "Which instrument is being played in this audio?",
    "What instrument sound can you hear in this audio?",
    "Which instrument is in this audio?",
    "Can you recognize the instrument in this audio?",
    "What instrument is this sound coming from?",
    "Can you identify the instrument playing in the audio?",
    "What instrument sound is being conveyed in this audio?",
    "What instrument is in this audio?",
    "Can you identify the instrument in this audio?",
    "Which instrument is playing in this audio?",
    "What instrument can you hear in this audio?",
    "What instrument is being played in the audio?",
    "Where is this instrument sound coming from?",
    "Can you identify the instrument in this audio?",
    "What instrument is coming from this audio?",
    "Can you hear the instrument playing in this audio?",
    "Which instrument is primarily being played in this audio?",
    "What instrument is being played in this audio?",
    "Can you identify the instrument in this audio?",
    "What instrument sound is in this audio?"
]

# Answer seeds
answer_seeds = [
    "It can be heard from this audio that it is",
    "You can hear from this audio that it is",
    "It can be heard from this segment of audio that it is",
    "You can hear from this segment of audio that it is",
    "It can be heard from this recording that it is",
    "You can hear from this recording that it is",
    "It can be heard from this segment of the recording that it is",
    "You can hear from this segment of the recording that it is",
    "It can be heard from this sound that it is",
    "You can hear from this sound that it is",
    "It can be heard from this segment of sound that it is",
    "You can hear from this segment of sound that it is",
    "It can be heard from this clip that it is",
    "You can hear from this clip that it is",
    "It can be heard from this segment of the clip that it is",
    "You can hear from this segment of the clip that it is",
    "It can be heard from this track that it is",
    "You can hear from this track that it is",
    "It can be heard from this segment of the track that it is",
    "You can hear from this segment of the track that it is"
]

# Translation dictionary with three translations for each instrument_family_str
translation_dict = {
    "reed": ["reed", "reed instrument", "reed pipe"],
    "mallet": ["mallet instrument", "struck instrument", "percussion instrument"],
    "keyboard": ["keyboard", "electronic keyboard"],
    "guitar": ["guitar", "six-string", "plucked instrument"],
    "organ": ["organ", "pipe organ", "electronic organ"],
    "bass": ["bass", "bass guitar"],
    "brass": ["brass instrument", "metal instrument"],
    "string": ["string", "bowed instrument"],
    "flute": ["flute", "transverse flute", "wind instrument"],
    "vocal": ["vocal", "vocal music"],
    "synth_lead": ["synth lead", "synth"]
}


# Thread-safe list and lock
result_list = []
lock = Lock()


def process_item(key, value):
  """Process a single key-value pair and generate a new JSON item."""
  instrument_family_str = value.get("instrument_family_str")
  translated_labels = random.choice(translation_dict[instrument_family_str])

  if random.random() < 0.6:
    answer_seed = f'{translated_labels.capitalize()}.'
  else:
    answer_seed = f'{random.choice(answer_seeds)} {translated_labels}.'

  new_item = {
      "audio": f"Nsynth/{key}.wav",
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
  with lock:
    result_list.append(new_item)
    # print(f"Processed {key}")


def main(json_file_path, output_file_path):
  # Read and parse the JSON file
  with open(json_file_path, 'r') as file:
    data = json.load(file)

  # Use ThreadPoolExecutor for multithreading
  with ThreadPoolExecutor(max_workers=8) as executor:
    futures = [executor.submit(process_item, key, value)
               for key, value in data.items()]

    # Wait for all threads to complete
    for future in as_completed(futures):
      future.result()

  # Save the results to a new JSON file
  with open(output_file_path, 'w', encoding='utf-8') as out_file:
    # json.dump(result_list, out_file, ensure_ascii=False, indent=4)
    json.dump(result_list, out_file, ensure_ascii=False, separators=(',', ':'))

  print(f"New JSON file saved to {output_file_path}")


# Run the main function
if __name__ == "__main__":
  json_file_path = "examples.json"  # Replace with your JSON file path
  # Replace with the desired output JSON file path
  output_file_path = "json/Nsynth_aqa_eng.json"
  main(json_file_path, output_file_path)
