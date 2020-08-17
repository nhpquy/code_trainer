import json

filename = "t.json"
print(filename)

with open(filename, encoding='utf-8') as train_data:
    train = json.load(train_data)

TRAIN_DATA = []
for data in train:
    ents = [tuple(entity) for entity in data['entities']]
    TRAIN_DATA.append((data['content'].replace("\xa0", ""), {'entities': ents}))

with open('{}'.format(filename.replace('json', 'txt')), 'w', encoding='utf-8') as write:
    write.write(str(TRAIN_DATA))

print('-------------Copy and Paste to spacy training-------------')
print()
print()
print()
print(TRAIN_DATA)
print()
print()
print()
print('--------------------------End-----------------------------')
