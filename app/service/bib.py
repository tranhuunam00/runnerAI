from doctr.io import DocumentFile
from doctr.models import ocr_predictor
model = ocr_predictor(pretrained=True)


def detectTextFromImage(request):
  single_img_doc = DocumentFile.from_images("./input/detectFace/chay.jpg")
  result = model(single_img_doc)
  return result