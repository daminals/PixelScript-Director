import openai
import json, re
import random
from moviepy.editor import AudioFileClip, VideoFileClip, ImageSequenceClip
from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": "/tmp"})
import os
import subprocess

import codecs
from boto3 import Session
from boto3 import resource
from boto3 import client

s3 = resource('s3')
bucket_name = 'gpt3-video-scripts'
bucket = s3.Bucket(bucket_name)
# Create an S3 client
s3_client = client('s3')

def search_items_in_bucket(bucket_name, folder_name):
    # List objects in the bucket
    try:
        response = s3_client.list_objects_v2(
            Bucket=bucket_name,
            Prefix=folder_name
        )

        # Check if objects were found
        if 'Contents' in response:
            # print(response['Contents'])
            matching_items = [obj['Key'] for obj in response['Contents'] if re.match(r'^\d+\.png$', obj['Key'].split('/')[-1])]
            # Sort items based on the numeric part of their names
            matching_items.sort(key=lambda x: int(re.search(r'\d+', x.split('/')[-1]).group()))
            return matching_items
        else:
            return []

    except Exception as e:
        print(f"Error listing objects: {e}")
        return []

def download_file_from_s3(bucket, key, local_path):
    s3_client.download_file(bucket, key, local_path)

# COMBINE IMAGE FILES INTO A VIDEO
def combine_video_files(input_files, input_audio, output_file):
    # Check if there are input files
    if not input_files:
        print("No input files provided.")
        return
      
    # generate an 8 digit number
    random_number = random.randint(10000000, 99999999)
    
    audio_tmp_dir = f'/tmp/audio_files{random_number}'
    os.makedirs(audio_tmp_dir, exist_ok=True)
      
    # Download input audio from S3 to the temporary directory
    local_audio = f"{audio_tmp_dir}/audio.mp3"
    print(f"local audio: {local_audio}")
    download_file_from_s3(bucket_name, input_audio, local_audio)
    
    # Create a temporary directory to store downloaded files
    video_tmp_dir = f'/tmp/video_files{random_number}'
    os.makedirs(video_tmp_dir, exist_ok=True)

    # Download input files from S3 to the temporary directory
    local_files = []
    for s3_key in input_files:
        local_path = os.path.join(video_tmp_dir, os.path.basename(s3_key))
        download_file_from_s3(bucket_name, s3_key, local_path)
        local_files.append(local_path)
        
    # Calculate frame rate dynamically based on the number of images and audio duration
    num_images = len(local_files)
    audio_duration = AudioFileClip(local_audio).duration
    frame_rate = num_images / audio_duration

    # Create a text file listing the image files for ffmpeg
    image_list_file = '/tmp/image_list.txt'
    with open(image_list_file, 'w') as f:
        for image in local_files:
            f.write(f"file '{image}'\n")

    output_path = f'/tmp/output{random_number}.mp4'

    # Use ffmpeg to create the video
    ffmpeg_command = [
        'ffmpeg',
        '-r', f'{frame_rate}',  # Dynamic frame rate
        '-f', 'concat',
        '-safe', '0',
        '-i', image_list_file,
        '-i', local_audio,
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-strict', 'experimental',
        '-b:a', '192k',  # Adjust audio bitrate as needed
        output_path
    ]

    try:
      subprocess.run(ffmpeg_command, check=True)
    except subprocess.CalledProcessError as e:
      print(f"An error occurred: {e}")
      return

    # Upload to S3
    s3_client.upload_file(output_path, bucket_name, output_file)
    return


def lambda_handler(event, context):
    folder_name = event['folder_name']
    print(f"Folder name: {folder_name}")
    audio_file = f"{folder_name}/output.mp3"
    all_videos = search_items_in_bucket(bucket_name, folder_name + "/video")
    combine_video_files(all_videos, audio_file, f'{folder_name}/output.mp4')
    print("Done")
    return {
        'statusCode': 200,
        'body': json.dumps('')
    }
