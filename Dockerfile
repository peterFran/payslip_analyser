FROM python:3-onbuild
RUN apt-get update && apt-get -y install git ghostscript python-pil tesseract-ocr && apt-get clean
