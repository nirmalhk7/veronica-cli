import os
import pickle
from rich.console import Console
import spacy
from rich.table import Table
import yaml

statements={}


for file in os.listdir("corpus"):
    with open("corpus/{}".format(file), "r") as stream:
        try:
            x= yaml.safe_load(stream)
            for i in x["conversations"]:
                statements[i[0]]=file

        except yaml.YAMLError as exc:
            print(exc)

# print(statements)

nlp= pickle.load(open("veronica/data/en_core_web_md","rb"))
mod= pickle.load(open("veronica/data/module.weights","rb"))
# print(mod)
# nlp=spacy.load("veronica/data/en_core_web_md")
yescount=0
allcount=len(statements.keys())
hsx={}

table = Table()
table.add_column("File")
table.add_column("Question")
table.add_column("Similarity")
table.add_column("Mapped Function")
table.add_column("Statement Intent")
table.add_column("Category")

for statement in statements.keys():
    d1= nlp(statement)
    max_similarity=-1
    max_similarity_command=None
    for i in mod.keys():
        similarity= round(d1.similarity(i),2)
        if(round(similarity,2)>=0.80 and similarity>max_similarity):
            max_similarity=similarity
            max_similarity_command= mod[i]
    if(max_similarity!=-1):
        yescount+=1
        table.add_row(
            str(statements[statement]),
            str(statement),
            str(max_similarity),
            str(max_similarity_command),
            str(d1.ents),
            str(d1.cats)
        )

        if max_similarity_command in hsx:
            hsx[max_similarity_command]+=1
        else:
            hsx[max_similarity_command]=1

console= Console()
console.print(table)
print(yescount,allcount)
print(hsx)