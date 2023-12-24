[![Deploy to Amazon Lambda](https://github.com/daminals/PixelScript-Director/actions/workflows/aws.yml/badge.svg)](https://github.com/daminals/PixelScript-Director/actions/workflows/aws.yml) ![github repo badge: Cloud Provider](https://img.shields.io/badge/Cloud%20Provider-AWS-181717?color=orange) ![github repo badge: Language](https://img.shields.io/badge/Language-Python-181717?color=blue)
# PixelScript Director - AI Movie Generator

## Overview

PixelScript Director is a cloud-driven project designed to automatically create movies using artificial intelligence. The system leverages various AWS services, including Lambda, Polly, and S3, to generate dynamic content based on a script generated through OpenAI's fine-tuning model. Additionally, DALL·E 3 is employed for image generation to bring the script to life.

## Demo

The project is available for access [here](https://pixelscript.danielkogan.xyz/)

The materials used in the demonstration are available [here](https://drive.google.com/drive/folders/1QrklSuCbuILiERnr61DIrsoIyLKlNsua?usp=share_link)

## Architecture

Since the goal of the project overall was to create an all-in-one experience for AI Video Generation, it was then necessary to pick tools which would allow for the most seamless experience. 

Therefore, the backend of the project is based heavily on serverless microservice architecture, which allows for the project to be easily scalable and maintainable, as well as cost-effective. Lambdas seemed to be the most natural fit for the core backend component, especially as it integrated very well with other AWS services that were necessary from the start, such as text to speech with Polly, as well as easy storage. Since all of these components could be managed and accessed utilizing roles and permissions, it was very easy to integrate them into the project.

The frontend of the project is based on a simple HTML page, which allows for the user to easily interact with the backend. The frontend is hosted on Cloudflare Pages, which allows for easy deployment and hosting of static sites, and integrates directly with the codebase on GitHub. The frontend is responsible for calling the script generation and movie generation endpoints.

Below are the various components of the project and how they interact with each other:

### AWS Lambda Functions:
- Script Generation Lambda: Utilizes OpenAI's fine-tuning model to generate a movie script based on user-provided inputs.
- Image Generation Lambda: Leverages DALL·E 3 to create images corresponding to scenes in the generated script.
- Audio Synthesis Lambda: Utilizes AWS Polly to convert the script into spoken audio.
- Audio Combination Lambda: Combines the generated audio to an mp3 file.
- Movie Rendering Lambda: Combines the generated images and audio to create a final mp4 file.

### AWS S3 Bucket:
Utilize a public S3 bucket to store all generated content, including the script, images, and audio. The lambdas will all write to the bucket

### AWS API Gateway:
There are two API endpoints: one for script generation and one for movie generation. The script generation endpoint will trigger the script generation lambda. This will display on the frontend, which will allow the user to modify the script as they please. Afterwards, the user can then trigger the generate video lambda, which calls upon the audio synthesis and image generation lambdas. When those are complete, then they will trigger the audio combination lambda and video rendering lambda respectively.

### Amazon Polly & Transcribe:
Amazon Polly is used to convert the script into spoken audio. Amazon Transcribe is used to convert the spoken audio into text. Unfortunately, there is currently no setting for Polly to directly output SRT captioning files, so we must use Transcribe to convert the audio back into text for the purposes of captioning the video.

### AWS Elastic Container Registry:
The dependencies for the combined audio and video rendering lambda are too large to be deployed directly to AWS Lambda via layer. Therefore, the lambda is deployed as a Docker container to ECR.

### Cloudflare Pages:
The frontend HTML is displayed and hosted on Cloudflare Pages. The frontend is responsible for calling the script generation and movie generation endpoints.

### Architecture Diagram:
![Architecture Diagram](https://github.com/daminals/PixelScript-Director/blob/master/frontend/architecture_diagram.png?raw=true)


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

## Known Issues

Occasionally, the final video will be corrupt, with the last few seconds of audio being cut. This may be an issue with the amount of storage available to the lambda, or perhaps the way various components of the video are downloaded to the lambda. This issue is still a WIP.