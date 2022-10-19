FROM python:3.8-slim-buster

EXPOSE 8501

RUN mkdir -p /app
COPY . /app
WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "streamlit", "run", "/app/FileProcess.py", "--server.port=8501", "--server.address=0.0.0.0" ]
