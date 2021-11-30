
def unit(label,entityRequired=False):
    def wrapper(function):
        if(type(label)!=list):
            label_arr=[label]
        else:
            label_arr=label  
        
        setattr(function,'nlp',label_arr)
        setattr(function,'entityRequired',entityRequired)
        return function
    return wrapper