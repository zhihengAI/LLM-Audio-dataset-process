import os
import json
import random
import threading

question_seeds = [
    'Analyze the content of this audio.',
    'Describe this audio in detail.',
    'Describe this audio.',
    'Describe this audio.',
    'Analyze the content of this audio.',
    'Tell me about the specific content of this audio.',
    'Help me interpret the content of this audio.',
    'What is the main content of this audio?',
    'Explain the content of this audio in detail.',
    'Specifically describe the content of this audio.',
    'Analyze this audio.',
    'Explain the content of this audio in detail for me.',
    'Interpret the details of this audio.',
    'Describe the main information in this audio in detail.',
    'What is the content of this audio? Describe it in detail.',
    'Please analyze this audio in detail.',
    'Help me explain the detailed content of this audio.',
    'What is the detailed content of this audio?',
    'Interpret this audio in detail.',
    'Describe the specific content of this audio.',
    'What is the specific content of this audio? Describe it.',
    'Please analyze the information in this audio in detail.',
    'Specifically explain the content of this audio.',
    'Describe the content of this audio in detail.',
    'Analyze the specific content of this audio.',
    'Analyze this audio in detail.',
    'Describe every detail of this audio in detail.',
    'Please explain the content of this audio in detail.',
    'Can you describe this audio in detail?',
    'Analyze the content of this audio in detail.',
    'Explain every detail of this audio in detail.',
    'Please describe all the content of this audio.',
    'Help me analyze the content of this audio.',
    'Explain all the information in this audio in detail.',
    'Please describe this audio in detail.',
    'Describe the details of this audio in detail.',
    'Explain the content of this audio in detail.'
]

# Define the mapping from instrument_family_str to Chinese translations
translation_dict = {
    "bass": ["bass guitar", "bass"],
    "drums": ["drumming", "percussion"],
    "vocals": ["vocals", "human pure voice"],
    "other": ["other", "noise", "background sound"],
    "mixture": ["singer singing", "music", "song"]
}


def process_file(file_path, folder_name, results):
  instrument = os.path.splitext(os.path.basename(file_path))[
      0]  # Get the filename as the instrument
  translated_labels = random.choice(
      translation_dict.get(instrument, ["unknown"]))  # Get a random translation

  if translated_labels[0].lower() in 'aeiou':
    article = 'an'
  else:
    article = 'a'

  answer_seed = f'There is {article} {translated_labels} sound.'

  # Construct the JSON object
  data = {
      "audio": f"musdb18hq/{folder_name}/{instrument}.wav",
      "conversations": [
          {
              "from": "human",
              "value": random.choice(question_seeds),  # Ignore question_seeds
              "input_modality": "audio"
          },
          {
              "from": "gpt",
              "value": f'{answer_seed}',
              "output_modality": "text"
          }
      ]
  }
  results.append(data)  # Add the result to the list
  # print(f"Processed: {file_path}")  # Print processing information


# Define the main function to traverse the folder and perform multithreading processing
def main():
  base_dir = "test"
  results = []
  threads = []

  for root, dirs, files in os.walk(base_dir):
    for file in files:
      if file.endswith(".wav"):
        if 'other' in file or 'mixture' in file:
          continue
        folder_name = os.path.relpath(root, base_dir)
        file_path = os.path.join(root, file)

        # Create and start a new thread
        thread = threading.Thread(
            target=process_file, args=(file_path, folder_name, results))
        threads.append(thread)
        thread.start()

        # Limit the number of threads
        if len(threads) >= 8:
          for thread in threads:
            thread.join()  # Wait for the thread to complete
          threads = []

  # Wait for all threads to complete
  for thread in threads:
    thread.join()

  # Save the results to a JSON file
  with open("json/musdb18hq_caption_test_eng.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, separators=(',', ':'))

  print("Processing complete. Results saved to output.json")


if __name__ == "__main__":
  main()
