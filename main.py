from fastapi import FastAPI
from pdf2text import PdfConverter
from summarizer import Summarizer
from utils import pre_processing
from cleantext import clean
import time

from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/")
def root(pdf_path:str, ratio:float):
    start = time.time()
    pdf2txt = PdfConverter()
    doc = pdf2txt.convert_pdf2txt(pdf_path)
    text = pre_processing(doc)
    text = clean(text)
    model = Summarizer(model = 'distilbert-base-uncased')
    summ_text = model(text, min_length = 40, ratio = ratio)  # Specified with ratio
    end = time.time()-start
    return JSONResponse({'summ_text':summ_text, 'raw_text':text})


if __name__ == '__main__':
    root(pdf_path = 'C:/Users/akhatova/PycharmProjects/tmp/test3.pdf', ratio = 0.2)


