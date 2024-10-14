import json
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

# Question seeds
question_seeds = [
    'Analyze the content of this audio.',
    'Describe this audio in detail.',
    'Describe this audio.',
    'Describe this piece of audio.',
    'Explain the content of this audio.',
    'Tell me the specific content of this audio.',
    'Help me interpret the content of this audio.',
    'What is the main content of this audio?',
    'Explain the content of this audio in detail.',
    'Describe the content of this audio specifically.',
    'Analyze this audio.',
    'Give me a detailed explanation of the content of this audio.',
    'Interpret the details of this audio.',
    'Describe the main information of this audio in detail.',
    'What is the content of this audio? Describe it specifically.',
    'Please analyze this audio in detail.',
    'Help me explain the detailed content of this audio.',
    'What is the detailed content of this audio?',
    'Interpret this audio in detail.',
    'Talk about the specific content of this audio.',
    'What is the specific content of this audio? Describe it.',
    'Please analyze the information in this audio in detail.',
    'Explain the content of this audio specifically.',
    'What is the content of this audio in detail?',
    'Explain the specific content of this audio.',
    'Analyze this audio in detail.',
    'Describe every detail of this audio in detail.',
    'Please explain the content of this audio in detail.',
    'Can you describe this audio in detail?',
    'Analyze the content of this audio specifically.',
    'Explain every detail of this audio in detail.',
    'Please describe the full content of this audio.',
    'Help me analyze the content of this audio.',
    'Explain all the information in this audio in detail.',
    'Please describe this audio in detail.',
    'Describe the details of this audio specifically.',
    'Explain the content of this audio in detail.'
]

# Define dictionary mapping with three translations for each instrument_family_str
translation_dict = {
    "reed": ["reed", "reed pipe", "reed instrument"],
    "mallet": ["mallet instrument", "struck instrument", "percussion instrument"],
    "keyboard": ["keyboard instrument", "electronic keyboard"],
    "guitar": ["guitar", "six-string", "plucked instrument"],
    "organ": ["organ", "pipe organ", "electronic organ"],
    "bass": ["bass", "bass guitar"],
    "brass": ["brass instrument", "metal instrument"],
    "string": ["string instrument", "bowed instrument"],
    "flute": ["flute", "transverse flute", "wind instrument"],
    "vocal": ["vocal", "vocal music"],
    "synth_lead": ["synth lead", "synth sound"]
}

# Thread-safe list and lock
result_list = []
lock = Lock()


def process_item(key, value):
  """Process a single key-value pair and generate a new JSON item."""
  instrument_family_str = value.get("instrument_family_str")
  translated_labels = random.choice(translation_dict[instrument_family_str])

  # Check if the translated label starts with a vowel sound
  if translated_labels[0].lower() in 'aeiou':
    article = 'an'
  else:
    article = 'a'

  if random.random() < 0.5:
    answer_seed = f'{translated_labels.capitalize()} is playing.'
  else:
    answer_seed = f'There is {article} {translated_labels} sound.'

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
  output_file_path = "json/Nsynth_caption_eng.json"
  main(json_file_path, output_file_path)
