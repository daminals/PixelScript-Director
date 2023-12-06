# upload to AWS
aws ecr get-login-password | docker login -u AWS --password-stdin "https://$(aws sts get-caller-identity --query 'Account' --output text).dkr.ecr.us-east-1.amazonaws.com"

docker build --platform linux/amd64 -t moviepy .
docker tag moviepy:latest 318710067667.dkr.ecr.us-east-1.amazonaws.com/moviepy:latest
docker push 318710067667.dkr.ecr.us-east-1.amazonaws.com/moviepy:latest

aws lambda update-function-code --function-name combine_video --image-uri 318710067667.dkr.ecr.us-east-1.amazonaws.com/moviepy:latest  > /dev/null 2>&1