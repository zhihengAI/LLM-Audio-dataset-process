import os
import json
import random
from concurrent.futures import ThreadPoolExecutor

question_seeds = [
    'What is the tone and emotion of the speaker in this audio?',
    'What tone and emotion is the speaker using in the audio?',
    'Analyzing the audio, what is the tone and emotion of the speaker?',
    'From the tone and emotion in the audio, what can be inferred about the speaker’s emotion?',
    'What feeling does the speaker’s tone and emotion convey in the audio?',
    'After listening to this audio, what is the speaker’s tone and emotion?',
    'What emotion is expressed by the speaker in this audio?',
    'From the tone and emotion in the audio, what can be inferred about the speaker’s emotion?',
    'What emotion is conveyed by the speaker in the audio?',
    'Can the speaker’s emotion be felt in this audio?',
    'From this audio, what can be inferred about the speaker’s emotion?',
    'Identify the speaker’s emotion from the tone and emotion in the audio.',
    'What is the emotion of the speaker in this audio?',
    'What are the emotional characteristics of the speaker in this audio?',
    'Can the speaker’s emotion be heard in the audio?',
    'What tone and emotion is the speaker using in the audio?',
    'What emotion is reflected by the speaker’s tone and emotion in the audio?',
    'From this audio, what emotion is the speaker expressing?',
    'What emotion is conveyed by the speaker’s tone and emotion in the audio?',
    'What is the speaker’s emotion in this audio?',
    'What emotion is the speaker conveying in the audio?',
    'What can be heard about the speaker’s emotion from the audio?',
    'From this audio, what can be inferred about the speaker’s emotion?',
    'Can the speaker’s emotion be heard in the audio?',
    'What is the emotion of the speaker in the audio?'
]

answer_seeds = [
    'Listening to the audio, it can be felt that',
    'From the audio, it can be judged that',
    'From the audio, it can be heard that',
    'From the audio, it can be felt that',
    'When listening to this audio, it can be heard that',
    'From this audio, it is clearly evident that',
    'The audio conveys that',
    'From this recording, it can be felt that',
    'After listening to the audio, it can be concluded that',
    'The audio clearly indicates that',
    'Listening to this recording, it can be inferred that',
    'From listening to this audio, it can be noticed that',
    'From the sound in the audio, it can be sensed that',
    'From the tone in the audio, it can be heard that',
    'From the content of the audio, it can be recognized that',
    'From the sound in this audio, it can be heard that',
    'From the details in the audio, it can be perceived that',
    'After listening to this audio, you will notice that',
    'The audio reveals that',
    'From the recording, it is not difficult to hear that',
    'From the tone and emotion in the audio, it can be heard that',
    'This audio gives the feeling that',
    'Listening to this audio, it can be felt that',
    'From this recording, it can be clearly perceived that',
    'From the content of the audio, it can be heard that',
    'From the expression in the audio, it can be judged that',
    'From the recording, it can be clearly sensed that',
    'Listening to this recording, you will find that',
    'From the tonal changes in the audio, it can be heard that',
    'From the tone and emotion in this audio, it can be felt that',
]

emotion_map = {
    "angry": ["angry", "furious", "irritated", "annoyed"],
    "disgust": ["disgusted", "repulsed", "nauseated", "resentful"],
    "fear": ["fearful", "afraid", "terrified", "anxious"],
    "happy": ["happy", "joyful", "glad", "content"],
    "neutral": ["calm", "neutral", "composed", "unmoved"],
    "pleasant_surprised": ["pleasantly surprised", "delighted", "amazed", "excited"],
    "surprised": ["surprised", "shocked", "astonished", "taken aback"],
    "sad": ["sad", "downcast", "sorrowful", "melancholic"],
}


def process_audio_file(parent_folder_name, audio_name):
  # Extract the emotion and key part of the audio name
  emotion_english = parent_folder_name.split('_')[-1]
  audio_key = audio_name.split('_')[1].replace(".wav", "")

  # Randomly choose a Chinese translation from the emotion_map
  emotion_chinese_options = emotion_map.get(
      emotion_english.lower(), ["unknown emotion"])
  emotion_chinese = random.choice(emotion_chinese_options)

  answer_seed = f'{random.choice(answer_seeds)} her emotion is'
  if random.random() < 0.6:
    answer_seed = 'The speaker\'s emotion is'

  # Generate the JSON structure
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
              "value": f'{answer_seed} {emotion_chinese}.',
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
  with open('json/TESS_eng.json', 'w', encoding='utf-8') as f:
    # json.dump(json_results, f, ensure_ascii=False, indent=4)
    json.dump(json_results, f, ensure_ascii=False, separators=(',', ':'))

  print("All files processed and saved to audio_data.json.")


if __name__ == "__main__":
  root_dir = "TESS"
  process_folder(root_dir)
