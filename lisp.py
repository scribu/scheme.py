def fn_print(*args):
    print ', '.join(args)

def fn_if(cond, antecedent, consequent):
    if cond:
        return antecedent
    else:
        return consequent

def is_fn(token):
    return 'fn_' + token in globals()

def call_fn(token, args):
    return globals()['fn_' + token](*args)

def eval(token):
    if list == type(token):
        if not token:
            return token

        if is_fn(token[0]):
            return call_fn(token[0], [eval(arg) for arg in token[1:]])

        return [eval(arg) for arg in token]
    else:
        return token
