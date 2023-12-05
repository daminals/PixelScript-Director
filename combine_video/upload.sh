# upload to AWS
docker build --platform linux/amd64 -t moviepy .
docker tag moviepy:latest 318710067667.dkr.ecr.us-east-1.amazonaws.com/moviepy:latest
docker push 318710067667.dkr.ecr.us-east-1.amazonaws.com/moviepy:latest

aws lambda update-function-code --function-name combine_video --image-uri 318710067667.dkr.ecr.us-east-1.amazonaws.com/moviepy:latest  > /dev/null 2>&1