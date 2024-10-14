import os
import json
import random
import threading

question_seeds = [
    "Is there any instrument playing in this audio?",
    "What instrument is playing in the audio?",
    "What instrument is this sound from?",
    "Can you hear what instrument is playing in this audio?",
    "What instrument is being played in the audio?",
    "Where does this sound come from, which instrument?",
    "What instrument is featured in this audio?",
    "Can you identify the instrument in this audio?",
    "What instrument is this sound coming from in the audio?",
    "What instrument is playing in this audio?",
    "What instrument can be heard in the audio?",
    "Which instrument is featured in this audio?",
    "Can you tell what instrument is in this audio?",
    "Which instrument is making this sound?",
    "Can you recognize the instrument playing in the audio?",
    "What instrument's sound is conveyed in this audio?",
    "Which instrument is featured in this audio?",
    "Can you identify the instrument in the audio?",
    "What instrument is playing in this audio?",
    "What instrument can you hear in this audio?",
    "What instrument is playing in the audio?",
    "Where does the instrument sound come from in this audio?",
    "Can you identify the instrument in the audio?",
    "What instrument is playing in the audio?",
    "Can you hear the instrument playing in this audio?",
    "What is the main instrument in this audio?",
    "Which instrument is playing in this audio?",
    "Can you identify the instrument in this audio?",
    "What instrument's sound is coming from this audio?"
]

answer_seeds = [
    "You can hear that it is ",
    "It can be heard that it is ",
    "It is recognizable from the audio that it is ",
    "From this audio, you can hear that it is ",
    "It can be heard from this recording that it is ",
    "You can tell from this recording that it is ",
    "It can be recognized from this recording that it is ",
    "From this recording, you can hear that it is ",
    "It can be heard from this sound that it is ",
    "You can tell from this sound that it is ",
    "It can be recognized from this sound that it is ",
    "From this sound, you can hear that it is ",
    "You can hear from this clip that it is ",
    "It can be heard from this clip that it is ",
    "It can be recognized from this clip that it is ",
    "From this clip, you can hear that it is ",
    "It can be heard from this track that it is ",
    "You can tell from this track that it is ",
    "It can be recognized from this track that it is ",
    "From this track, you can hear that it is "
]

# Define the mapping from instrument_family_str to Chinese translations
translation_dict = {
    "bass": ["bass guitar", "bass"],
    "drums": ["drums", "percussion"],
    "vocals": ["vocals", "pure human voice"],
    "other": ["other", "noise", "background"],
    "mixture": ["singer singing", "music", "song"]
}



def process_file(file_path, folder_name, results):
  instrument = os.path.splitext(os.path.basename(file_path))[
      0]  # Get the filename as the instrument
  translated_labels = random.choice(
      translation_dict.get(instrument, ["Unknown"]))  # Get a random translation

  if random.random() < 0.6:
    answer_seed = f'{translated_labels.capitalize()}'
  else:
    answer_seed = f'{random.choice(answer_seeds)}{translated_labels} sound'

  # Construct the JSON object
  data = {
      "audio": f"musdb18hq/{folder_name}/{instrument}.wav",
      "conversations": [
          {
              "from": "human",
              "value": random.choice(question_seeds),
              "input_modality": "audio"
          },
          {
              "from": "gpt",
              "value": f'{answer_seed}.',
              "output_modality": "text"
          }
      ]
  }
  results.append(data)


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
  with open("json/musdb18hq_aqa_test_eng.json", "w", encoding="utf-8") as f:
    # json.dump(results, f, ensure_ascii=False, indent=4)
    json.dump(results, f, ensure_ascii=False, separators=(',', ':'))

  print("Processing complete. Results saved to output.json")


if __name__ == "__main__":
  main()
