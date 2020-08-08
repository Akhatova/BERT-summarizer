import os
import glob
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from urllib.request import urlopen
from io import StringIO, BytesIO
import re


class PdfConverter(object):

    def __init__(self):
        self.output_path = ''

    @staticmethod
    def convert_pdf2txt(filename):
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec = codec, laparams = laparams)
        if filename.startswith('http'):
            f = urlopen(filename).read()
            fp = BytesIO(f)
        else:
            fp = open(filename, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos = set()
        for page in PDFPage.get_pages(fp, pagenos, maxpages = maxpages, password = password, caching = caching,
                                      check_extractable = True):
            interpreter.process_page(page)
        text = retstr.getvalue()
        fp.close()
        device.close()
        retstr.close()
        return text

    def save_pdf2txt(self, file_path):
        """
        run and save .pdf document as .txt
        """
        output = self.convert_pdf2txt(file_path)
        output_name = re.sub("\.pdf", ".txt", file_path.split('/')[-1])
        print("conversion of "+ output_name)
        #with open(os.path.join(self.output_path, output_name), "w", encoding = 'utf-8') as f:
            #f.write(output)
        return output

    def pdf2txt_multi(self, dir_path):
        """
        run a nd save all .pdf documents from dir_path directory as .txt files)
        """
        filelist = glob.glob(dir_path + "/*.pdf")
        for filename in filelist:
            print("conversion of " + filename.split("/")[-1])
            output = self.convert_pdf2txt(dir_path+filename)
            output_name = re.sub("\.pdf", ".txt", self.file_path)
            with open(os.path.join(self.output_path, output_name), "w", encoding = 'utf-8') as f :
                f.write(output)
