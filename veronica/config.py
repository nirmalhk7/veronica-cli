
units={}
def unit(synonyms=[]):
    def decorator(method):
        unit.method=method
        synonyms.append(method.__name__)
        for synonym in synonyms:
            units[synonym]= method
        print(units)
    return decorator