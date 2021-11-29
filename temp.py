import yaml
import json

statements=[]
with open("corpus/humor.yml", "r") as stream:
    try:
        x= yaml.safe_load(stream)
        for i in x["conversations"]:
            statements.append(i[1])
    except yaml.YAMLError as exc:
        print(exc)

print(json.parse(statements))