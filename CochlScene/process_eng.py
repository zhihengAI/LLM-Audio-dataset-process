import os
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



no_answer_seeds = [
    'No noticeable sounds were detected in this audio.',
    'The audio does not contain any recognizable sounds.',
    'There are no sounds present in this audio.',
    'This audio does not have any detectable sound.',
    'The analysis shows no sounds in this audio.',
    'This audio file is silent and contains no sounds.',
    'No sounds were found in this audio recording.',
    'The audio appears to be completely silent.',
    'There are no audible elements in this audio.',
    'No sound events were identified in this audio.',
    'This audio does not produce any noise.',
    'The audio file is devoid of any sounds.',
    'No sound can be heard in this audio.',
    'The recording contains no sounds.',
    'This audio clip is empty and has no sound.',
    'No auditory signals were detected in this audio.',
    'This audio is silent; no sounds are present.',
    'No acoustic events are found in this audio.',
    'This audio recording is completely silent.',
    'There are no noise elements in this audio.',
    'The audio does not include any sound.',
    'This audio file does not contain any sound.',
    'No audio signals were detected in the recording.',
    'The audio recording is silent with no sound.',
    'No acoustic signals were found in this audio.',
    'The sound analysis indicates silence in this audio.',
    'This audio does not feature any sounds.',
    'No discernible sounds are present in this audio.',
    'This audio recording does not have any sound.',
    'The audio is silent, with no sounds detected.'
]

# 文件夹名称与包含不同表达方式的地点翻译映射，每个包含5个选项
folder_translation = {
    "Bus": ["on the bus", "inside a bus", "aboard a bus", "near the bus stop", "next to a bus"],
    "Cafe": ["in a cafe", "at a cafe", "inside a coffee shop", "near a cafe", "beside a coffeehouse"],
    "Car": ["inside a car", "in a vehicle", "near a car", "next to a parked car", "beside an automobile"],
    "CrowdedIndoor": ["in a crowded indoor space", "inside a crowded venue", "around a busy hall", "near a bustling indoor area", "beside a crowded room"],
    "Elevator": ["in an elevator", "inside a lift", "next to an elevator", "near an elevator door", "beside a lift"],
    "Kitchen": ["in the kitchen", "inside a kitchen", "near the cooking area", "around the kitchen", "beside a kitchen"],
    "Park": ["in the park", "inside a park", "near a playground", "beside the park entrance", "around a public garden"],
    "ResidentialArea": ["in a residential area", "inside a residential neighborhood", "around a housing area", "near a living community", "beside a suburban street"],
    "Restaurant": ["in a restaurant", "at a dining place", "inside a bistro", "near a restaurant", "beside a food venue"],
    "Restroom": ["inside a restroom", "in the bathroom", "near a lavatory", "next to a washroom", "beside a public restroom"],
    "Street": ["on the street", "along the road", "near the pavement", "around the corner of a street", "beside the road"],
    "Subway": ["on the subway", "inside a subway car", "near a metro station", "next to a subway platform", "around the subway station"],
    "SubwayStation": ["in the subway station", "at a metro station", "near a transit station", "around a metro terminal", "beside an underground station"]
}


def process_audio_file(file_path):
  parent_folder = os.path.basename(os.path.dirname(file_path))
  grandparent_folder = os.path.basename(
      os.path.dirname(os.path.dirname(file_path)))
  audio_name = os.path.basename(file_path)

  translated_folder = random.choice(folder_translation.get(
      parent_folder, ['']))

  if random.random() < 0.6:
    answer_seed = ''
    translated_folder = translated_folder.capitalize()
  else:
    answer_seed = random.choice(answer_seeds) + ' '

  gpt_value = f'{answer_seed}{translated_folder}.'
  if not translated_folder:
    gpt_value = random.choice(no_answer_seeds)

  json_item = {
      "audio": f"CochlScene/{grandparent_folder}/{parent_folder}/{audio_name}",
      "conversations": [
          {
              "from": "human",
              "value": random.choice(question_seeds),
              "input_modality": "audio"
          },
          {
              "from": "gpt",
              "value": f'{gpt_value}',
              "output_modality": "text"
          }
      ]
  }

  return json_item


def find_audio_files(base_folder):
  audio_files = []
  for root, dirs, files in os.walk(base_folder):
    for file in files:
      if file.endswith('.wav'):
        audio_file_path = os.path.join(root, file)
        audio_files.append(audio_file_path)
  return audio_files


def main():
  base_folder = "./CochlScene"
  audio_files = find_audio_files(base_folder)

  json_results = []

  with ThreadPoolExecutor(max_workers=8) as executor:
    results = executor.map(process_audio_file, audio_files)

    for result in results:
      json_results.append(result)

  output_file = 'json/CochlScene_eng.json'
  with open(output_file, 'w', encoding='utf-8') as json_file:
    json.dump(json_results, json_file, ensure_ascii=False, indent=4)
    # json.dump(json_results, json_file, ensure_ascii=False, separators=(',', ':'))

  print(f"All JSON data has been saved to {output_file}")


if __name__ == "__main__":
  main()
