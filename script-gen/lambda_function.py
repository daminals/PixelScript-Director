import openai
import json
import os
import random

import codecs
from boto3 import Session
from boto3 import resource

session = Session(region_name="us-east-1")
polly = session.client("polly")

s3 = resource('s3')
bucket_name = 'gpt3-video-scripts'
bucket = s3.Bucket(bucket_name)

openai.api_key = os.environ["OPENAI_API_KEY"]


def generate_video_script(director, topic):
    response = openai.ChatCompletion.create(
        model="ft:gpt-3.5-turbo-1106:personal::8R6vhAys",
        messages=[
            {"role": "system", "content": f"MovieAI is a masterful filmmaker which emulates famous directors in order to create new twists on old concepts and films. It will return the response in the following format: Seperate scenes by using \"Scene 1\n\" where 1 corresponds to the scene number and clearly indicate who is currently speaking by utilizing \"Voice 1:\n\" where 1 corresponds to the number of the character currently speaking"},
            {"role": "user", "content": f"In the style of {director}, write {topic}. Seperate scenes by using \"Scene 1\n\" where 1 corresponds to the scene number and clearly indicate who is currently speaking by utilizing \"Voice 1:\n\" where 1 corresponds to the number of the character currently speaking"}
        ],
    )
    return response.choices[0]['message']['content']

# def split_script(script):
#   # split the script into multiple voices with each voice indicated by a newline, a colon, voice and the number of this character currently speaking
#   # Example:
#   # \n Voice 1:
#   lines = script.split("\\n")
#   result = {}
#   current_voice = None
#   i = 0
#   voiceCount = 0
#   while i < len(lines):
#       line = lines[i]
#       if line.startswith("Voice"):
#           current_voice = line.strip()
#           if current_voice not in result:
#               result[current_voice] = []
#       else:
#           line_length = len(line)
#           if current_voice is not None:
#             result[current_voice].append([voiceCount, line.strip()])
#             voiceCount += 1
#       i += 1
#   return result
# Example usage
# script = """
# Voice 1:
# Hello
# Voice 2:
# Hi
# Voice 1:
# Bingo
# """


def split_script(script):
    # read everything here as voice 1: "\nVoice 1:\n"
    # split the script into multiple voices with each voice indicated by a newline, a colon, voice and the number of this character currently speaking
    lines = script.split("\n")
    result = []
    current_voice = None
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("Voice"):
            current_voice = line.strip()
        elif line.startswith("Scene"):
            pass  # ignore scene
        else:
            if current_voice is not None:
                result.append([current_voice, line.strip()])
        i += 1
    return result


def process_script(script_arr):
    voiceIDs = [
        "Matthew",
        "Russell",
        "Nicole",
        "Emma",
        "Aria",
        "Kendra",
        "Kimberly",
        "Joey",
        "Justin"
    ]
    voices = {}
    line_num = 0

    for voice_obj in script_arr:
        voice, line = voice_obj
        if voice not in voices:
            voiceID = random.choice(voiceIDs)
            voices[voice] = voiceID
            voiceIDs.remove(voiceID)

        # now process the audio
        filename = f"voice{line_num}.mp3"
        try:
            tts(line, voices[voice], filename)
        except:
            print(f"{voices[voice]} is a failure")
        line_num += 1


def tts(text, voiceId, filename):
    response = polly.synthesize_speech(
        Text=text,
        OutputFormat="mp3",
        VoiceId=voiceId
    )
    stream = response["AudioStream"]
    bucket.put_object(Key=filename, Body=stream.read())


def lambda_handler(event, context):
    topic = event['topic']
    director = event['director']
    # video_script = generate_video_script(director, topic)
    # Example usage
    # topic = "space exploration"
    # director = "Steven Spielberg"
    video_script = generate_video_script(director, topic)
    split_script_result = split_script(video_script)
    # return {"video_script":video_script, "split_script_result":split_script_result}
    process_script(split_script_result)
    return {
        'statusCode': 200,
        'body': json.dumps(split_script_result)
    }
