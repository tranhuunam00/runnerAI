from retinaface import RetinaFace
from flask import Flask, request
import os
import cv2
from threading import Thread


app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

output_folder = "cropped_faces"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)


@app.route('/')
def hello_world():
    return 'Hello World'


def remove_file(file_path):
    os.remove(file_path)

@app.route('/', methods=['POST'])
def detectFace():
    if 'file' not in request.files:
        return 'Không tìm thấy file'

    file = request.files['file']
    print(file)

    if file.filename == '':
        return 'Không tìm thấy tên file'

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    imBRG = cv2.imread(file_path)
    imRGB = cv2.cvtColor(imBRG, cv2.COLOR_BGR2RGB)

    obj = RetinaFace.detect_faces(file_path)
    for key in obj.keys():
        identity = obj[key]
        facial_area = identity["facial_area"]

        cropped_face = imRGB[facial_area[1]:facial_area[3], facial_area[0]:facial_area[2]]
        cropped_face_rgb = cv2.cvtColor(cropped_face, cv2.COLOR_BGR2RGB)
        # Lưu khuôn mặt đã cắt
        cv2.imwrite(os.path.join(output_folder, "cropped_face_" +
                    str(key) + ".jpg"), cropped_face_rgb)
    t = Thread(target=remove_file, args=(file_path,))
    t.start()
    return "hehe"


if __name__ == '__main__':
    app.run()
