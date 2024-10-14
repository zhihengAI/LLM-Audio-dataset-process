import os
import json
import random
import concurrent.futures

# Simulated question_seeds and answer_seeds
question_seeds = [
    'What is the tone and emotion of the speaker in this audio?',
    'What kind of tone and emotion is the speaker using in the audio?',
    'Analyzing the audio, what is the tone and emotion of the speaker?',
    'Based on the tone and emotion in the audio, what can you infer about the speaker’s emotion?',
    'What feeling does the speaker’s tone and emotion in the audio give?',
    'After listening to this audio, what is your judgment of the speaker’s tone and emotion?',
    'What emotion is expressed by the speaker in this audio?',
    'What emotion can be deduced from the tone and emotion in the audio?',
    'What kind of emotion does the speaker convey in the audio?',
    'Can you sense the speaker’s emotion in this audio?',
    'Based on this audio, what is the speaker’s emotion?',
    'Identify the speaker’s emotion based on the tone and emotion in the audio.',
    'How is the speaker’s emotion in this audio?',
    'What emotional characteristics are displayed by the speaker in this audio?',
    'Can you hear the speaker’s emotion in the audio?',
    'What kind of tone and emotion is the speaker using in the audio?',
    'What emotion is reflected by the speaker’s tone and emotion in the audio?',
    'Based on this audio, what emotion is the speaker expressing?',
    'What emotion is displayed by the speaker’s tone and emotion in the audio?',
    'What is the speaker’s emotion in this audio?',
    'What emotion is the speaker expressing in the audio?',
    'What can be heard as the speaker’s emotion in the audio?',
    'Based on this audio, what is the speaker’s emotion?',
    'Can you hear what emotion the speaker is expressing in the audio?',
    'How is the speaker’s emotion in the audio?'
]

answer_seeds = [
    'From the audio, it can be sensed that the speaker',
    'The audio indicates that the speaker',
    'It can be heard from the audio that the speaker',
    'The audio suggests that the speaker',
    'While listening to the audio, it can be heard that the speaker',
    'This audio clearly shows that the speaker',
    'The audio conveys that the speaker',
    'This recording suggests that the speaker',
    'After listening to the audio, it can be deduced that the speaker',
    'The audio clearly indicates that the speaker',
    'Listening to this recording, it can be inferred that the speaker',
    'Based on this audio, it can be found that the speaker',
    'The sound in the audio suggests that the speaker',
    'The tone in the audio suggests that the speaker',
    'Based on the content of the audio, it can be identified that the speaker',
    'The sound in this audio suggests that the speaker',
    'The details in the audio suggest that the speaker',
    'After listening to this audio, it can be noticed that the speaker',
    'The audio reveals that the speaker',
    'The recording clearly shows that the speaker',
    'The tone and emotion in the audio indicate that the speaker',
    'This audio gives the impression that the speaker',
    'Listening to this audio, it can be felt that the speaker',
    'This recording clearly suggests that the speaker',
    'Based on the content of the audio, it can be heard that the speaker',
    'The expression in the audio suggests that the speaker',
    'The recording clearly suggests that the speaker',
    'Listening to this recording, it can be found that the speaker',
    'The tone and emotion in this audio suggest that the speaker'
]

# Gender dictionary
gender_prefix = {
    "bea": "her emotion is",
    "jenie": "her emotion is",
    "josh": "his emotion is",
    "sam": "his emotion is"
}

# Emotion translation dictionary
emotion_translation = {
    "Amused": ["amused", "happy", "entertained", "delighted", "joyful"],
    "Angry": ["angry", "mad", "irritable", "upset", "annoyed"],
    "Disgusted": ["disgusted", "irritated", "grossed out", "discontented", "repulsed"],
    "Neutral": ["neutral", "calm", "composed", "indifferent", "unemotional"],
    "Sleepy": ["sleepy", "drowsy", "tired", "sleepy and sluggish", "sleepy and lethargic"]
}


def process_audio_file(parent_folder_name, audio_name):
  # print(f"Processing file: {audio_name} in folder: {parent_folder_name}")

  # Extract emotion keyword
  name_prefix = parent_folder_name.split('_')[0]
  emotion_keyword = parent_folder_name.split('_')[1]
  emotion_chinese = random.choice(
      emotion_translation.get(emotion_keyword, [""]))
  gender_text = gender_prefix.get(name_prefix, [""])

  answer_seed = f'{random.choice(answer_seeds)} {gender_text} '

  if random.random() < 0.6:
    answer_seed = ''

  # Construct JSON dictionary
  json_dict = {
      "audio": f"EmoV_DB/{parent_folder_name}/{audio_name}",
      "conversations": [
          {
              "from": "human",
              "value": random.choice(question_seeds),
              "input_modality": "audio"
          },
          {
              "from": "gpt",
              "value": f'{answer_seed}{emotion_chinese}.',
              "output_modality": "text"
          }
      ]
  }

  return json_dict


def process_all_files(directory):
  json_data = []

  # Use 8 threads
  with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
    futures = []

    # Traverse directory and files
    for parent_folder_name in os.listdir(directory):
      parent_folder_path = os.path.join(directory, parent_folder_name)
      if os.path.isdir(parent_folder_path):
        for audio_name in os.listdir(parent_folder_path):
          if audio_name.endswith('.wav'):
            # Submit task to thread pool
            futures.append(
                executor.submit(process_audio_file,
                                parent_folder_name, audio_name)
            )

    # Retrieve processing results
    for future in concurrent.futures.as_completed(futures):
      json_data.append(future.result())

  return json_data


# Main function
if __name__ == "__main__":
  directory = "EmoV_DB"  # Replace with the actual folder path
  result = process_all_files(directory)

  # Save results as JSON file
  with open("json/EmoV_DB_eng.json", "w", encoding="utf-8") as f:
    # json.dump(result, f, ensure_ascii=False, indent=4)
    json.dump(result, f, ensure_ascii=False, separators=(',', ':'))

  print("Processing complete. JSON file saved as EmoV_DB_en.json")
