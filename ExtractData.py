# -*- coding: utf-8 -*-
"""
Created on Tue May 12 10:57:57 2015

@author: Bohan Zhang
"""
import xml.etree.ElementTree as ET
import re, os
from bs4 import BeautifulSoup

'''Function to get clean XBRL tag'''
def getTag(text):
    '''Remove the url between {}'''
    urlText = re.findall('\\{(.*?)\\}',text)
    TextToRemove = '{'+str(urlText).strip("['']")+'}'
    cleanedTag = text.replace(TextToRemove,"")
    return cleanedTag
        
'''Function to get clean text: to remove html tags in the text'''
def getCleanText(text):
    ''' Add a space after >'''
    newText = re.sub(r'(?![(a-z)])([>])', r'\1 ', text)
    soup = BeautifulSoup(newText)
    cleantext=soup.text.strip()
    cleanText = ' '.join(cleantext.split())
    return cleanText

'''Function to output plain footnote file'''
def parseFile(InFile, InPath, OutPath):
    
    filePath = InPath +'/' +InFile
    tree = ET.parse(filePath)
    root = tree.getroot()
        
    n = len(root)
    Filing = []    
    for i in range(n):
        key = root[i].tag
        content = root[i].text
        data = [key,content]
        Filing.append(data)
            
    '''Remove blanks'''
    FilingCleaned = [x for x in Filing if (x[1] is not None and x[1] != '\n    ')]
           
    '''Filing Data'''   
    XBRLTags = [getTag(x[0]) for x in FilingCleaned]
    Tags = [re.sub(r"(?<=\w)([A-Z])", r" \1", x) for x in XBRLTags]
    Contents = [getCleanText(x[1]) for x in FilingCleaned]
    
    '''Footnote Data'''
    Footnote = []
    nTag = len(XBRLTags)
    for i in range(nTag):
        '''Footnote: lenght>20'''
        if len(Contents[i]) > 20:
            FootnoteXBRLTag = XBRLTags[i]
            FootnoteTag = Tags[i]
            FootnoteContent = Contents[i]
            footnote = [FootnoteXBRLTag,FootnoteTag,FootnoteContent]
            Footnote.append(footnote)
            
    # FootnoteXBRLTags = [x[0] for x in Footnote]
    FootnoteTags = [x[1].replace(' Text Block','') for x in Footnote]
    FootnoteContents = [x[2].encode('ascii','ignore') for x in Footnote]
            
    nOut = len(FootnoteTags)
    flag = InFile.find('.')
    OutFile = OutPath + InFile[:flag] + '-Footnote.txt'
    with open(OutFile,'a') as output_file:
        for i in range(0,nOut):
            output_file.write(FootnoteTags[i]+'\n')
            output_file.write(FootnoteContents[i]+'\n'+'\n')
        
InPath_neg = 'C:/Users/Bohan Zhang/Desktop/GWU/Course/2015 Spring/Practicum/get_data/10-K/neg'
OutPath_neg = 'C:/Users/Bohan Zhang/Desktop/GWU/Course/2015 Spring/Practicum/extract report/10-K/neg/'
Filings_neg = os.listdir(InPath_neg)

for i in range(29,len(Filings_neg)):
    InFile = Filings_neg[i]
    parseFile(InFile, InPath_neg, OutPath_neg)
    
InPath_pos = 'C:/Users/Bohan Zhang/Desktop/GWU/Course/2015 Spring/Practicum/get_data/10-K/pos'
OutPath_pos = 'C:/Users/Bohan Zhang/Desktop/GWU/Course/2015 Spring/Practicum/extract report/10-K/pos/'
Filings_pos = os.listdir(InPath_pos)

for i in range(0,len(Filings_pos)):
    InFile = Filings_pos[i]
    parseFile(InFile, InPath_pos, OutPath_pos)





