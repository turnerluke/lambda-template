# lambda base image for Docker from AWS
FROM public.ecr.aws/lambda/python:latest
LABEL authors="turner"
# copy all code and lambda handler
COPY src/ .
COPY lambda_handler.py ./
COPY requirements.txt ./
# COPY config.py ./
COPY config.yaml ./
# install packages
RUN yum install -y gcc-c++ pkgconfig poppler-cpp-devel
RUN python3 -m pip install -r requirements.txt
# run lambda handler
CMD ["lambda_handler.handler"]