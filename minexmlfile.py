# -*- coding: utf-8 -*-
__author__ = 'pangbochen'

import os
from xml.dom.minidom import parse
import xml.dom.minidom

outputfileName = 'data/abstract_1000_2015.txt'
filename = ""
output = open(outputfileName, 'w', encoding='utf-8')

rootDir = 'E:\\LDA\\NSF\\NSF\\2015'
filelist = os.listdir(rootDir)
print(len(filelist))

xml_cnt = 0

for i in range(len(filelist)):
    # for text case pick 1000 xml abstract file as the input
    if xml_cnt > 1000:
        break
    xml_cnt+=1
    #TODO delete later

    path = os.path.join(rootDir, filelist[i])
    if os.path.isfile(path):
        DOMTree = xml.dom.minidom.parse(path)
        Data = DOMTree.documentElement
        Abstracts = Data.getElementsByTagName("AbstractNarration")
        if len(Abstracts)>0 and len(Abstracts[0].childNodes):
            abstract = Abstracts[0].childNodes[0].data
            output.write(abstract + ' \n')
            print(path)

output.close()

print('end')








print('end')