import sys

def fn_display(expr):
    print expr,

def fn_concat(args):
    return ''.join(args)

def fn_list(*args):
    return args

forms = {
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
    'cons': lambda x, lst: [x] + list(lst),

    'null?': lambda x: not x,

    'string-concatenate': fn_concat,

    'number->string': str,

    'display': fn_display,
    'newline': lambda: sys.stdout.write("\n")
}

def call(scope, name, args):
    evald_args = [scope.eval(arg) for arg in args]
    return forms[name](*evald_args)
