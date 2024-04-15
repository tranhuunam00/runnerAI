# Base image for Python Flask
FROM python:3.11-bullseye

# Python environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /flask-app

# Copy the requirements file
COPY ./requirements.txt .

COPY retinaface.h5 /root/.deepface/weights/
COPY vgg_face_weights.h5 /root/.deepface/weights/

RUN apt-get update
RUN apt install -y libgl1-mesa-glx

# Install the dependencies
RUN pip install -r requirements.txt




# Copy the Flask app file
COPY . .

EXPOSE 5000


VOLUME ["/flask-app"]

COPY db_resnet50-84171458.zip /root/.cache/doctr/models/
COPY crnn_vgg16_bn-76b7f2c6.zip /root/.cache/doctr/models/



RUN pip install tf2onnx



# Run the Flask app
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]