# coding: utf8
import matplotlib

import pandas as pd
import matplotlib.pyplot as plt
import random
import spacy
from xlwt import Workbook
wb = Workbook()
model_path = 'Data/Test'
nlp = spacy.load(model_path)

# test_text = open('../named_entity_recognition/spacy-ner-annotator-master/timviec365new.txt',  encoding="utf8").read()
test_text = u"Đọc, hiểu, viết thành thạo tài liệu tiếng anh"
doc = nlp(test_text)
# file = open('kq.xlsx', 'w')
# file.write('kq.xlsx', )
for ent in doc.ents:
    print(ent.label_, ent.text)
if doc.ents is ():
    print('No entity is recognized')

