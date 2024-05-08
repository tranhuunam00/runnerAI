from retinaface import RetinaFace
from flask import Flask, request
import os
import cv2
from threading import Thread
from deepface import DeepFace

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

output_folder = "cropped_faces"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

sample_folder = "sample_folder"

def remove_file(file_path):
    os.remove(file_path)


def detectFace(request):
    if 'file' not in request.files:
        return 'Không tìm thấy file'

    file = request.files['file']
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

        cropped_face = imRGB[facial_area[1]
            :facial_area[3], facial_area[0]:facial_area[2]]

        cropped_face_rgb = cv2.cvtColor(cropped_face, cv2.COLOR_BGR2RGB)

        # Lưu khuôn mặt đã cắt
        cv2.imwrite(os.path.join(output_folder, str(key) + "__" +
                                 file.filename), cropped_face_rgb)
    t = Thread(target=remove_file, args=(file_path,))
    t.start()
    return {
        "code": 200,
        "data": "success"
    }


def findFace(request):
    if 'file' not in request.files:
        return 'Không tìm thấy file'

    file = request.files['file']
    if file.filename == '':
        return 'Không tìm thấy tên file'

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    form = request.form
    eventId = form.get('eventId')

    folder = sample_folder + eventId
    if not os.path.exists(folder):
        os.makedirs(folder)
        
    images = DeepFace.find(img_path=file_path, db_path=folder, enforce_detection = False)

    if(len(images) == 1): 
        return []
    res = []
    for image in images:
        if (float(image["distance"]) < 0.15):
            print("---")
            res.append(image.values[0][0])

    t = Thread(target=remove_file, args=(file_path,))
    t.start()
    return res
