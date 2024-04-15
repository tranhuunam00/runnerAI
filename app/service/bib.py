from doctr.io import DocumentFile
from doctr.models import ocr_predictor
import os
from threading import Thread

from app.service.face import remove_file

model = ocr_predictor(pretrained=True)
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def detectTextFromImage(request):
  if 'file' not in request.files:
        return 'Không tìm thấy file'

  file = request.files['file']
  if file.filename == '':
      return 'Không tìm thấy tên file'

  file_path = os.path.join(UPLOAD_FOLDER, file.filename)
  file.save(file_path)
  single_img_doc = DocumentFile.from_images(file_path)
  t = Thread(target=remove_file, args=(file_path,))
  t.start()
  
  result = model(single_img_doc)
  words = []
  
  for page in result.pages:
    for block in page.blocks:
      for line in block.lines:
        for word in line.words:
          if(word.confidence  > 0.7):
            words.append(word.value)
  return words