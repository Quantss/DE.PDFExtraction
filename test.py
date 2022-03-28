
from dataclasses import replace
from unittest import result
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

page = 391

with pdfplumber.open(fund) as pdf:
    page = pdf.pages[int(page) + 2]
    text = page.extract_text().split('\n')

# text[12].split('EUR')

##############################
# Extraction
##############################


currency = ['EUR', 'DKK', 'USD']
totalDelimiter = ['TOTAL', 'Total']
securities = []

equities = []


for i in text:

    cur = [ele for ele in currency if (ele in i)]
    element = {}

    if len(cur) == 0:
        continue

    elif len(cur) == 1:

        if any(str in i for str in totalDelimiter):

            replacedWord = i.replace('Total', 'TOTAL')

            if replacedWord.index('TOTAL') == 0:

                splitWord = replacedWord.split(cur[0])[1]
                splitValues = splitWord.split(' ')
                element['Currency'] = cur[0]
                element['Quantity'] = splitValues[0]
                element['Entity'] = splitValues[1]
                element['Market Value'] = splitValues[2]

            else:

                splitWord = replacedWord.split('TOTAL')[0]
                splitWordCur = splitWord.split(cur[0])[1]
                splitValues = splitWordCur.split(' ')
                element['Currency'] = cur[0]
                element['Quantity'] = splitValues[0]
                element['Entity'] = splitValues[1]
                element['Market Value'] = splitValues[2]

        else:
            splitCur = i.split(cur[0])[1:]
            for k in splitCur:
                splitValues = k.split(' ')
                element['Currency'] = cur[0]
                element['Quantity'] = splitValues[0]
                element['Entity'] = splitValues[1]
                element['Market Value'] = splitValues[2]


    equities.append(element)

    else:
        

        
for i in text:
    cur = [ele for ele in currency if (ele in i)]
    element = {}
    print(cur)

    if len(cur) == 0:
        continue

    elif len(cur) == 1:
        continue
    else:
        print(len(cur))
        for l in cur:
            curRef = len(cur)

            