from stdlib import functions

def eval(token):
    if list == type(token):
        if not token:
            return token

        if token[0] in functions:
            evald_args = [eval(arg) for arg in token[1:]]
            return functions[token[0]](*evald_args)

        return [eval(arg) for arg in token]
    else:
        return token
