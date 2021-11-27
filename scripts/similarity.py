

nlp=spacy.load("en_core_web_md")
while True:
    d1= nlp(input("S1 = "))
    d2= nlp(input("S2 = "))
    print(d1.similarity(d2))