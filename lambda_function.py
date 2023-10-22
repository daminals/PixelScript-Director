import openai
import json
import os

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
      model="gpt-3.5-turbo",
      # model="text-davinci-003",
      messages=[
        {"role": "system", "content": f"You are {director}, genius and master of script writing"},
        {"role": "user", "content": f"Write a script for a 30 second video about {topic}. Only include the dialogue and narration."}
      ]
    )
    return response.choices[0]['message']['content']

def tts(text):
  filename = "test.mp3"
  response = polly.synthesize_speech(
    Text=text,
    OutputFormat="mp3",
    VoiceId="Matthew"
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
    tts(video_script)
    return {
        'statusCode': 200,
        'body': json.dumps(video_script)
    }