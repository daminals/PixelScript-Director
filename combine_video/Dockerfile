FROM public.ecr.aws/lambda/python:3.11

# copy the ffmpeg binary
COPY bin/ffmpeg /usr/local/bin/ffmpeg

# Copy requirements.txt
COPY requirements.txt ${LAMBDA_TASK_ROOT}

RUN apt-get update 
RUN apt-get wget
RUN wget https://mirrors.kernel.org/ubuntu/pool/main/libf/libffi/libffi6_3.2.1-8_amd64.deb && apt install ./libffi6_3.2.1-8_amd64.deb && apt install libffi-dev


# Install the latest pip
RUN pip install --upgrade pip setuptools wheel

# Install the specified packages
RUN pip install -r requirements.txt

# Copy function code
COPY lambda_function.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "lambda_function.lambda_handler" ]