
from dataclasses import replace
from unittest import result
from numpy import extract
import requests
import pdfplumber
import pandas as pd
import re

##############################
# Working Navigation
##############################

fund = "TestFiles\SEMREP-2021-06-30-EN-00-2021-08-25-106347697 - LUX.pdf"

page = 391

with pdfplumber.open(fund) as pdf:
    # page = pdf.pages[int(page)]
    page = pdf.pages[int(page) + 2]
    text = page.extract_text().split('\n')

# text[12].split('EUR')

#######################################
# Fund Search
#######################################


report = "TestFiles\SEMREP-2021-06-30-EN-00-2021-08-25-106347697 - LUX.pdf"

page = 0

pages = [0, 1, 2, 3]

# fundType = ['ETF', 'Equity']

funds = []


for page in pages:
    with pdfplumber.open(report) as pdf:
        text = pdf.pages[page].extract_text().split('\n')

        for i in text:
            fund = {}
            if 'Table of Contents' not in i:
                pass
                if 'Equity' in i:
                    splitPage = (i.split(' '))
                    name = splitPage[0]
                    pageSearch = splitPage[1]
                    # name = re.findall('[A-Z][^A-Z]*', name)
                    # # fundName = ' '.join(name)
                    #
                    fund['Name'] = name

                    fund['Page#'] = pageSearch

                    funds.append(fund)


##############################
# Extraction
##############################


currency = ['EUR', 'DKK', 'USD', 'MYR', 'PHP', 'PLN', 'PKR', 'MXN', 'AUD']
totalDelimiter = ['TOTAL', 'Total']
securities = []

equities = []


for i in text:

    cur = [ele for ele in currency if (ele in i)]
    element = {}

    # handling empty rows

    if len(cur) == 0:
        continue

    # If the row isn't empty (has at least one currency list)

    elif len(cur) == 1:

        # Removing 'Total row'

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

# handling multiple currenies

    else:

        curCopy = cur

        while len(curCopy) != 0:

            for l in cur:

                replaceCur = i.replace(l, '| ')

                curCopy.remove(l)

    equities.append(element)
