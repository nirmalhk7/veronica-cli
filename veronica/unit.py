
def unit(label, googleCredsNeeded=False):
    def wrapper(function):
        if(not isinstance(label, list)):
            label_arr = [label]
        else:
            label_arr = label

        setattr(function, 'nlp', label_arr)
        return function
    return wrapper
