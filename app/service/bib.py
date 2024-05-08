from doctr.io import DocumentFile
from doctr.models import ocr_predictor
import os
from threading import Thread
import cv2
from retinaface import RetinaFace

from app.service.face import remove_file

model = ocr_predictor(pretrained=True)
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


sample_folder = "sample_folder"


def detectTextFromImage(request):
    if 'file' not in request.files:
        return 'Không tìm thấy file'

    file = request.files['file']
    if file.filename == '':
        return 'Không tìm thấy tên file'

    form = request.form
    originName = form.get('fileName')
    eventId = form.get('eventId')

    folder = sample_folder + eventId
    if not os.path.exists(folder):
        os.makedirs(folder)

    file_path = os.path.join(folder, originName)
    file.save(file_path)
    single_img_doc = DocumentFile.from_images(file_path)

    obj = RetinaFace.detect_faces(file_path)

    result = model(single_img_doc)
    words = []

    for page in result.pages:
        for block in page.blocks:
            for line in block.lines:
                for word in line.words:
                    if (word.confidence > 0.7):
                        words.append(word.value)

  
    # nếu đủ điều kiện là ảnh mẫu thì không xóa
    if (len(words) != 0):
        if (len(obj.keys()) == 1):
            return words

    t = Thread(target=remove_file, args=(file_path,))
    t.start()
    return words
