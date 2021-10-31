

def component(func):
    func_call=func.__name__
    component.func_call=func
    return func