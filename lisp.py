from stdlib import native_fn

def is_list(token):
    return type(token) in [list, tuple]

def fn_if(cond, a, b):
    if eval(cond):
        return eval(a)

    return eval(b)

# todo: distinguish between symbols and strings
def eval(token):
    if is_list(token):
        if not token:
            return token

        if str == type(token[0]):
            if 'if' == token[0]:
                return fn_if(*token[1:])

            if 'def' == token[0]:
                return fn_def(*token[1:])

            if token[0] in native_fn:
                return native_fn_call(*token)

            if token[0] in user_fn:
                return user_fn_call(*token)

        return [eval(arg) for arg in token]
    else:
        return token

user_fn = {}

def fn_def(name, args, *body):
    if name in native_fn:
        print "Error: can't redefine '%s'; native function." % name
        return False

    user_fn[name] = {
        'args': args,
        'body': body
    }

def native_fn_call(name, *args):
    evald_args = [eval(arg) for arg in args]   # evaluate args before function body
    return native_fn[name](*evald_args)

def _bind_var(name, value, token):
    if is_list(token):
        return [_bind_var(name, value, t) for t in token]

    if token == name:
        return value

    return token

def user_fn_call(name, *args):
    fn = user_fn[name]

    body = fn['body']

    i = 0
    for arg_name in fn['args']:
        body = _bind_var(arg_name, eval(args[i]), body)
        i = i+1

    return eval(body)[-1]    # return value from last statement
