import os
import pickle
import spacy
import yaml

statements=[]


for file in os.listdir("corpus"):
    with open("corpus/{}".format(file), "r") as stream:
        try:
            x= yaml.safe_load(stream)
            for i in x["conversations"]:
                statements.append(i[0])

        except yaml.YAMLError as exc:
            print(exc)

# print(statements)

nlp= pickle.load(open("veronica/data/en_core_web_md","rb"))
mod= pickle.load(open("veronica/data/module.weights","rb"))
# print(mod)
# nlp=spacy.load("veronica/data/en_core_web_md")
yescount=0
allcount=len(statements)
for statement in statements:
    d1= nlp(statement)
    max_similarity=-1
    max_similarity_command=None
    for i in mod.keys():
        similarity= round(d1.similarity(i),2)
        if(similarity>=0.75 and similarity>max_similarity):
            max_similarity=similarity
            max_similarity_command= mod[i]
    if(max_similarity!=-1):
        yescount+=1
        print(statement,max_similarity,max_similarity_command)

print(yescount,allcount)