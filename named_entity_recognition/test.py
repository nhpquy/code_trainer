import spacy
from spacy.matcher import PhraseMatcher

model_path = 'Data/'
nlp = spacy.load(model_path)

matcher = PhraseMatcher(nlp.vocab, attr="SHAPE")
matcher.add("date", None, nlp("2016/11/25"), nlp("7/11/2019"), nlp("12/08/1999"), nlp("1/7/1999"), nlp("25/2/1999"),
            nlp("2016/1/25"), nlp("2016/1/6"), nlp("2016/11/9"), nlp("2016-11-25"), nlp("7-11-2019"), nlp("12-08-1999"),
            nlp("1-7-1999"), nlp("25-2-1999"), nlp("2016-1-25"), nlp("2016-1-6"), nlp("2016-11-9"), nlp("2016.11.25"),
            nlp("7.11.2019"), nlp("12.08.1999"), nlp("1.7.1999"), nlp("25.2.1999"), nlp("2016.1.25"), nlp("2016.1.6"),
            nlp("2016.11.9"))

date_found = []

doc = nlp("sinh ngày 15/9/1993 hay 1991-1-12")
for match_id, start, end in matcher(doc):
    print("Matched based on token shape:", str(doc[start:end]))
