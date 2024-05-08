# runnerAI
phần AI cho dự án runner


RUN pip install -r requirements.txt  --break-system-packages

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y


RUN pm2 start main.py --name flask-app --interpreter=python3