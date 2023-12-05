[![Deploy to Amazon Lambda](https://github.com/daminals/PixelScript-Director/actions/workflows/aws.yml/badge.svg)](https://github.com/daminals/PixelScript-Director/actions/workflows/aws.yml) ![github repo badge: Cloud Provider](https://img.shields.io/badge/Cloud%20Provider-AWS-181717?color=orange) ![github repo badge: Language](https://img.shields.io/badge/Language-Python-181717?color=blue)
# PixelScript Director - AI Movie Generator

## Overview

PixelScript Director is a cloud-driven project designed to automatically create movies using artificial intelligence. The system leverages various AWS services, including Lambda, Polly, and S3, to generate dynamic content based on a script generated through OpenAI's fine-tuning model. Additionally, DALL·E 3 is employed for image generation to bring the script to life.

## Architecture

The architecture of the project involves several key components:

### AWS Lambda Functions:
- Script Generation Lambda: Utilizes OpenAI's fine-tuning model to generate a movie script based on user-provided inputs.
- Image Generation Lambda: Leverages DALL·E 3 to create images corresponding to scenes in the generated script.
- Audio Synthesis Lambda: Utilizes AWS Polly to convert the script into spoken audio.
- Audio Combination Lambda: Combines the generated audio to an mp3 file.
- Movie Rendering Lambda: Combines the generated images and audio to create a final mp4 file.

## How It Works

1. User Input: Users provide the director with a corresponding plot. The plot is then used to generate a script in the style of their chosen director.
2. Script Generation:
The Script Generation Lambda uses OpenAI's fine-tuning model to generate a movie script based on user inputs.
3. Image Generation:
The Image Generation Lambda uses DALL·E 3 to create a series of images corresponding to scenes in the generated script.
4. Audio Synthesis:
The Audio Synthesis Lambda utilizes AWS Polly to convert the script into spoken audio.
5.  Audio Combination:
The Audio Combination Lambda combines the generated audio to an mp3 file.
6. Movie Rendering:
The generated images and audio are combined to create a movie file.
7. Storage:
All generated content, including the script, images, and audio, is stored in an S3 bucket for future reference.

## See It In Action

Go to [PixelScript Director](http://ams560-web.s3-website-us-east-1.amazonaws.com/) to see the project in action.