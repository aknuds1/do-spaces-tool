from python:alpine3.6

WORKDIR /app

RUN pip3 install -U boto3

COPY do-spaces-tool.py .

ENTRYPOINT ["python3", "do-spaces-tool.py"]
