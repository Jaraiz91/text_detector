FROM ubuntu:20.04
RUN mkdir /app
WORKDIR /app
COPY . /app
RUN apt-get update && apt-get install  -y python3.9
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get install -y pip && pip3 install -r requirements.txt
WORKDIR /app/src/scripts/
ENTRYPOINT ["python3", "text_detector.py"]