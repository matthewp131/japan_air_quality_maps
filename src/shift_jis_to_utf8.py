import codecs

with codecs.open("../data/TM20210000.txt", mode='r', encoding='shift_jisx0213') as file:
    lines = file.read()

with codecs.open("../data/TM20210000.csv", mode='w', encoding="utf-16") as file:
    for line in lines:
        file.write(line)