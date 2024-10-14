import os
import json
import random
import threading

question_seeds = [
    "How is the speaker's emotion in this audio?",
    "What kind of emotion does the speaker have in the audio?",
    "Analyzing the audio, what is the speaker's emotion?",
    "From the emotion in the audio, we can infer the speaker's emotion.",
    "What kind of feeling does the speaker's emotion in the audio convey?",
    "After listening to this audio, determine what the speaker's emotion is like.",
    "What emotion is expressed by the speaker in this audio?",
    "From the emotion in the audio, what can be inferred about the speaker's emotion?",
    "What kind of emotion does the speaker convey in the audio?",
    "Can you feel the speaker's emotion in this audio?",
    "From this audio, what can you infer about the speaker's emotion?",
    "Identify the speaker's emotion from the emotion in the audio.",
    "How is the speaker's emotion in this audio?",
    "What is the emotional characteristic of the speaker in this audio?",
    "Can you hear the speaker's emotion in the audio?",
    "What kind of emotion is the speaker using in the audio?",
    "What does the speaker's emotion reflect in the audio?",
    "From this audio, what emotion is the speaker expressing?",
    "What kind of emotion is the speaker showing in the audio?",
    "What kind of emotion is the speaker using in the audio?",
    "What can you hear about the speaker's emotion in the audio?",
    "From this audio, determine the speaker's emotion.",
    "Can you hear what emotion the speaker is expressing in the audio?",
    "How is the speaker's emotion in the audio?"
]

answer_seeds = [
    "The audio suggests that",
    "It can be inferred from the audio that",
    "You can hear from the audio that",
    "The audio conveys that",
    "Listening to this audio, you can tell that",
    "It's clear from the audio that",
    "The audio reveals that",
    "This recording suggests that",
    "After listening to the audio, you can conclude that",
    "The audio clearly indicates that",
    "From this recording, you can infer that",
    "From the sound in the audio, you can detect that",
    "The tone in the audio suggests that",
    "The content of the audio suggests that",
    "From the emotion in this audio, you can tell that",
    "This audio conveys that",
    "This audio suggests that",
    "This recording reveals that",
    "The audio indicates that",
    "This recording suggests that",
    "The emotion in this audio indicate that",
    "This audio suggests that",
    "This recording clearly shows that",
    "The content of the audio indicates that",
    "The tone in the audio suggests that",
    "The emotion in this recording reveal that",
    "Listening to this recording, you can tell that",
    "The emotion in this audio suggest that",
    "From the emotion in this audio, you can feel that"
]

# Emotion translations
emotion_translations = {
    "happy": ["happy", "joyful", "cheerful", "pleased", "delighted"],
    "assertive": ["assertive", "confident", "decisive", "determined", "self-assured"],
    "angry": ["angry", "furious", "annoyed", "irritated", "upset"],
    "apologetic": ["apologetic", "sorry", "remorseful", "regretful", "ashamed"],
    "encouraging": ["encouraging", "motivational", "supportive", "inspiring", "uplifting"],
    "neutral": ["neutral", "calm", "composed", "unemotional", "detached"],
    "excited": ["excited", "enthusiastic", "passionate", "eager", "animated"],
    "concerned": ["concerned", "worried", "anxious", "troubled", "uneasy"],
    "anxious": ["anxious", "nervous", "worried", "apprehensive", "uneasy"],
    "sad": ["sad", "sorrowful", "unhappy", "melancholic", "dejected"]
}

# Get all .txt files in the folder


def get_txt_files(folder):
  return [f for f in os.listdir(folder) if f.endswith('.txt')]

# Emotion processing logic for answers


def process_file(txt_file, folder, results):
  # Extract information from the filename
  base_name = os.path.splitext(txt_file)[0]
  parts = base_name.split('_')
  gender = parts[0] if len(parts) > 0 else ''
  emotion = parts[1] if len(parts) > 1 else ''

  # Determine the pronoun based on gender
  pronoun = ("her" if "female" in gender else "his") + ' emotion is'

  # Diverse emotion translation
  emotion_translation = random.choice(
      emotion_translations.get(emotion.lower(), [emotion]))

  answer_seed = f'{random.choice(answer_seeds)} {pronoun} '
  if random.random() < 0.6:
    answer_seed = ''

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
              "value": f'{answer_seed}{emotion_translation}.',
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

  # Wait for the remaining threads to finish
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
  output_folder = "json/JLcorpus_cls_eng.json"

  process_files_multithreaded(folder, output_folder, num_threads=8)
