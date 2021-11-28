import pickle
import spacy

nlp= pickle.load(open("veronica/data/en_core_web_md","rb"))
nlp=spacy.load("en_core_web_md")
while True:
    d1= nlp(input("S1 = "))
    d2= nlp(input("S2 = "))
    print("{} {} || {}".format(d1.ents,d2.ents,d1.similarity(d2)))