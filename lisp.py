from stdlib import native_fn

def is_list(token):
    return type(token) in [list, tuple]

def eval(token):
    if is_list(token):
        if not token:
            return token

        if token[0] in native_fn:
            evald_args = [eval(arg) for arg in token[1:]]
            return native_fn[token[0]](*evald_args)

        return [eval(arg) for arg in token]
    else:
        return token
