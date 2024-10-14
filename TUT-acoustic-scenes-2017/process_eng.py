import json
import random
from concurrent.futures import ThreadPoolExecutor

question_seeds = [
    "Where does this audio scene take place?",
    "In what kind of setting was this audio recorded?",
    "What kind of environment or location does the background sound in this recording suggest?",
    "Analyzing the sound clues in the audio, can you infer where this might be?",
    "Based on the sound characteristics in the audio, can you guess where the environment is?",
    "Do the background sounds and other clues in the audio indicate where this might be?",
    "What kind of scene would these sound effects in the audio likely occur in?",
    "What kind of place does the environmental sound in the audio remind you of?",
    "Can you infer the location where this audio was recorded based on the sound elements?",
    "After listening to this audio, what kind of environment do you think it takes place in?",
    "Based on the sound details in the audio, can you guess in what kind of scene this audio was recorded?",
    "Can the sound characteristics in the audio help you pinpoint the specific location of the recording?",
    "Do the sound effects in the audio bring any particular scene to mind?",
    "Considering the sound features in the audio, can you infer where this audio was recorded?",
    "By analyzing the sound clues in the audio, where do you think this recording might have taken place?",
    "From the background noise in the audio, can you guess what kind of environment this recording was made in?",
    "Where specifically do you think this audio was recorded based on the environment?",
    "Can the specific sounds and background noises in the audio help you infer the scene of this recording?",
    "Can you determine the environment based on the echoes and reverberations in the audio?",
    "What kind of environment or location do the captured sound elements in the audio suggest?",
    "After hearing the audio, can you deduce the specific scene of the recording?",
    "Based on the sound clues in the audio, what do you think the setting of this recording might be?",
    "Can you infer the location of the recording by analyzing the background sounds in the audio?",
    "By analyzing the specific sound clues in the audio, where do you think this recording took place?",
    "Can you deduce the specific location of the recording based on the sound effects and background noises?",
    "Can the various sound characteristics in the audio indicate where this recording was made?",
    "From the environmental sounds and background noise in the audio, where do you think this recording was made?",
    "Considering the various sound clues in the audio, can you guess what the recording location might be?",
    "Can you guess where this recording took place by analyzing the sound clues and environmental sound effects?",
    "Based on the sound characteristics in the audio, can you say where this recording was made?",
]

answer_seeds = [
    "The audio background suggests that it was recorded",
    "The background sounds indicate that the recording took place",
    "The recording seems to have occurred",
    "The scene of this recording appears to be",
    "The sounds suggest that the recording was made",
    "The audio was likely captured",
    "The recording seems to have taken place",
    "The audio indicates that the scene is",
    "The environment in the audio suggests a location",
    "The audio hints that it was recorded",
    "The sounds in the audio imply that the recording happened",
    "The audio clues point to a location",
    "The background noises suggest the recording was",
    "The soundscape indicates that this recording took place",
    "The ambiance in the audio suggests",
    "The recording environment appears to be",
    "The audio suggests the recording was made",
    "The context in the audio implies a location",
    "The recording setting seems to be",
    "The captured sounds suggest that the location is",
    "The recording likely took place",
    "The sounds in the audio suggest that it occurred",
    "The background audio hints at a location",
    "The audio suggests that the scene is",
    "The sound environment implies that the recording was",
    "The audio recording seems to have taken place",
    "The environment captured in the audio suggests",
    "The audio clues indicate that it was recorded",
    "The sounds captured in the recording point to",
    "The audio hints that the recording location is",
    "The background noise suggests the recording happened",
    "The recording seems to have been made",
    "The ambiance in the recording indicates",
    "The environment in the audio implies that it took place",
    "The audio background points to a setting"
]


translation_dict = {
    'home': ['home', 'at home', 'in the house', 'in the residence', 'inside the house'],
    'metro_station': ['metro station', 'near the metro', 'inside the metro station', 'metro entrance', 'metro station entrance'],
    'office': ['in the office', 'inside the company', 'at the workplace', 'inside the office', 'office area'],
    'bus': ['near the bus', 'near the coach', 'near the public bus', 'around the bus', 'near the bus stop'],
    'beach': ['by the beach', 'on the sand', 'by the sea', 'by the coastline', 'on the beach'],
    'city_center': ['city center', 'downtown', 'city core', 'busy district', 'central area'],
    'tram': ['near the tram', 'tram stop', 'tram station', 'on the tram', 'along the tramline'],
    'cafe/restaurant': ['inside the cafe/restaurant', 'inside the cafe', 'inside the restaurant', 'inside the dining place', 'in the coffee shop'],
    'residential_area': ['residential area', 'residential zone', 'living area', 'inside the community', 'by the residential complex'],
    'train': ['near the train', 'train station', 'inside the train carriage', 'on the train', 'by the railway'],
    'library': ['inside the library', 'in the library', 'library area', 'book house', 'reading room'],
    'forest_path': ['forest path', 'woodland trail', 'in the forest', 'along the wooded path', 'in the forest path'],
    'car': ['near the car', 'by the vehicle', 'next to the car', 'inside the car', 'outside the car'],
    'park': ['around the park', 'in the park', 'inside the park area', 'in the greenery', 'inside the amusement park'],
    'grocery_store': ['inside the grocery store', 'inside the convenience store', 'inside the supermarket', 'inside the food store', 'inside the grocery shop']
}


def process_line(line):
  parts = line.strip().split('\t')
  audio_file, cls_res, _ = parts[:3]

  # Randomly choose a translation from the translation_dict
  translated_cls_res_options = translation_dict.get(cls_res, [cls_res])
  translated_cls_res = random.choice(translated_cls_res_options)

  if random.random() < 0.6:
    answer_seed = ''
  else:
    answer_seed = random.choice(answer_seeds) + ' '

  gpt_value = f'{answer_seed}{translated_cls_res}.'

  return {
      "audio": audio_file.replace('audio/', 'TUT/'),
      "conversations": [
          {
              "from": "human",
              "value": random.choice(question_seeds),
              "input_modality": "audio"
          },
          {
              "from": "gpt",
              "value": gpt_value,
              "output_modality": "text"
          }
      ]
  }


def txt_to_json(txt_file_path, json_file_path):
  data = []

  with open(txt_file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

  # Use ThreadPoolExecutor for multithreading, with 9 threads
  with ThreadPoolExecutor(max_workers=8) as executor:
    futures = [executor.submit(process_line, line) for line in lines]
    for future in futures:
      data.append(future.result())

  with open(json_file_path, 'w', encoding='utf-8') as json_file:
    # json.dump(data, json_file, ensure_ascii=False, indent=4)
    json.dump(data, json_file, ensure_ascii=False, separators=(',', ':'))


if __name__ == '__main__':
  txt_to_json('meta.txt', 'json/TUT_Acoustic_scenes_eng.json')
