import sys
from lexer import Lexer, Symbol

class Lambda:

    def __init__(self, args, body):
        self.args = args
        self.body = body

    def __repr__(self):
        return str(self.body)

user_globals = {}

def special_define(token, value):
    user_globals[token.value] = eval(value)

def special_if(cond, a, b):
    if eval(cond):
        return eval(a)

    return eval(b)

def special_quote(expr):
    return expr

def special_lambda(args, *body):
    for arg in args:
        if not is_symbol(arg):
            raise Exception("Syntax error: '%s' is not a valid arg name" % arg)

    return Lambda(args, body)

def fn_display(expr):
    print expr,

def fn_concat(args):
    return ''.join(args)

def fn_list(*args):
    return args

forms_native = {
    '=': lambda a, b: a == b,
    '>': lambda a, b: a > b,
    '>=': lambda a, b: a >= b,
    '<': lambda a, b: a < b,
    '<=': lambda a, b: a <= b,
    'eq': lambda a, b: a == b,

    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
    '/': lambda a, b: a / b,
    '%': lambda a, b: a % b,

    'list': fn_list,
    'car': lambda a: a[0],
    'cdr': lambda a: a[1:],

    'string-concatenate': fn_concat,

    'number->string': str,

    'display': fn_display,
    'newline': lambda: sys.stdout.write("\n")
}

def is_list(token):
    return type(token) in [list, tuple]

def is_symbol(token):
    return isinstance(token, Symbol)

def forms_native_call(name, args):
    evald_args = [eval(arg) for arg in args]   # evaluate args before function body

    return forms_native[name](*evald_args)

def _bind_var(name, value, token):
    if is_list(token):
        return [_bind_var(name, value, t) for t in token]

    if not is_symbol(token):
        return token

    if token.value == name.value:
        return value

    return token

def user_fn_call(name, args):
    fn = user_globals[name]

    if not isinstance(fn, Lambda):
        raise Exception("'%s' is not callable" % name)

    body = fn.body

    i = 0
    for formal_arg in fn.args:
        body = _bind_var(formal_arg, eval(args[i]), body)
        i += 1

    # # DEBUG
    # if user_fn_call.calls > 20:
    #     import sys
    #     sys.exit()
    # user_fn_call.calls += 1

    return eval(body)[-1]    # return value from last statement

# DEBUG
# user_fn_call.calls = 0

def _find_forms(prefix, container):
    for key, value in globals().items():
        if key.startswith(prefix):
            container[ key[len(prefix):] ] = value

forms_special = {}
_find_forms('special_', forms_special)

def eval(thing):
    if not thing:
        return thing

    if is_list(thing):
        if is_symbol(thing[0]):
            value = thing[0].value

            if value in forms_special:
                return forms_special[value](*thing[1:])

            if value in forms_native:
                return forms_native_call(value, thing[1:])

            if value in user_globals:
                return user_fn_call(value, thing[1:])

            raise Exception("Undefined procedure: '%s'" % value)
        else:
            return [eval(arg) for arg in thing]

    if is_symbol(thing):
        if thing.value in user_globals:
            return user_globals[thing.value]
        else:
            raise Exception("Unbound variable: '%s'." % thing.value)

    return thing

def execute(fname):
    lexer = Lexer(fname)

    ast = lexer.get_ast(lexer.get_tokens())

    return eval(ast)

if __name__=="__main__":
    execute(sys.argv[1])
