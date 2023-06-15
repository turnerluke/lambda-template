# lambda base image for Docker from AWS
FROM public.ecr.aws/lambda/python:latest
LABEL authors="turner"


# Copy all code and lambda handler
COPY src/ .
COPY lambda_handler.py .
COPY config.yaml .
COPY requirements.txt .
COPY tests .
COPY _submodules _submodules


# Install packages
# Install all submodules
RUN find _submodules/* -maxdepth 0 -type d -exec pip install --upgrade {}/ \;
# Install other packages
RUN python3 -m pip install -r requirements.txt
# Install pytest if used in project
RUN python3 -m pip install pytest


# Specify the Lambda Handler
CMD ["lambda_handler.handler"]