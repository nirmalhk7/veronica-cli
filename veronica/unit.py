
def unit(label):
    def wrapper(function):
        if(type(label)!=list):
            label_arr=[label]
        else:
            label_arr=label    
        setattr(function,'nlp',label_arr)
        return function
    return wrapper