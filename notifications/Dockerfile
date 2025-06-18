FROM public.ecr.aws/lambda/python:latest

WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY notification_maker.py .
COPY notification_lambda.py .

CMD ["notification_lambda.lambda_handler"]