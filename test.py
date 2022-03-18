from numpy import extract
import requests
import pdfplumber
import pandas as pd


def download_file(url):
    local_filename = url.split('/')[-1]

    # with requests.get(url) as r:
    #     r.raise_for_status()
    #     with open(local_filename, 'wb') as f:
    #         f.write(r.content)

    return local_filename

##############################
# Working Navigation
##############################


# import PyPDF2

# with open("TestFiles\SEMREP-2021-06-30-EN-00-2021-08-25-106347697 - LUX.pdf", 'rb') as pdfFile:
#     pdfReader = PyPDF2.PdfFileReader(pdfFile)

#     pdfPage = pdfReader.getPage(394)
#     extracted = pdfPage.extractText()

# extracted


fund = "TestFiles\SEMREP-2021-06-30-EN-00-2021-08-25-106347697 - LUX.pdf"


with pdfplumber.open(fund) as pdf:
    page = pdf.pages[391]
    text = page.extract_text().split('\n')

# text[12].split('EUR')

##############################
# Extraction
##############################


currency = ['EUR', 'DKK', 'USD']

securities = []

for i in currency:
    for j in text:
        if i in j:
            divideTranche = j.replace(i, '| ')
            print(divideTranche)


for i in text:
    result = [ele for ele in currency if (ele in i)]
    for j in result:
        divideTranche = i.replace(j, '| ')
        splitTranche = divideTranche.split('| ')
        print(result)

        



