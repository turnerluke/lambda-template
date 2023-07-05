# lambda base image for Docker from AWS
FROM public.ecr.aws/lambda/python:latest
LABEL authors="turner"

# copy all dependencies
COPY src src
COPY tests tests
COPY _submodules _submodules

COPY config.yaml .
COPY lambda_handler.py .
COPY requirements.txt .
COPY setup.py .

# Install packages
# Install this project
RUN python3 -m pip install .
# Install all submodules
RUN find _submodules/* -maxdepth 0 -type d -exec pip install --upgrade {}/ \;
# Install other packages
RUN python3 -m pip install -r requirements.txt
# Install pytest if used in project
RUN python3 -m pip install pytest

# Specify the Lambda Handler
CMD ["lambda_handler.handler"]
