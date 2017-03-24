# -*- coding: utf-8 -*-
import time
import random
#because the platform is Windows , use clock() instead of time(), which is recommanded in class

#as
#asa

import os
from xml.dom.minidom import parse
import xml.dom.minidom

outputfileName = 'result/abstract.txt'
filename = "E:\\LDA\\NSF\\NSF\\2015\\1500662.xml"

DOMTree = xml.dom.minidom.parse(filename)
Data = DOMTree.documentElement
Abstracts = Data.getElementsByTagName("AbstractNarration")
abstrac = Abstracts[0].childNodes[0].data

