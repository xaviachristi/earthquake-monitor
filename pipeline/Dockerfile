# syntax=docker/dockerfile:1
FROM public.ecr.aws/lambda/python:latest

RUN dnf -y update && \
    dnf install -y \
    gcc \
    gcc-c++ \
    make \
    libffi-devel \
    libxml2-devel \
    libxslt-devel \
    lapack-devel \
    blas-devel \
    libcurl-devel \
    libsndfile \
    && dnf clean all

WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY extract.py .
COPY transform.py .
COPY load.py .
COPY pipeline.py .

CMD [ "pipeline.lambda_handler" ]