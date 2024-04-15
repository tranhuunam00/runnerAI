from doctr.io import DocumentFile
from doctr.models import ocr_predictor
model = ocr_predictor(pretrained=True)


def detectTextFromImage(request):
  single_img_doc = DocumentFile.from_images("./input/detectFace/chay.jpg")
  print("quaaaaaaa---------")
  result = model(single_img_doc)
  print(result)
  return "heheh"