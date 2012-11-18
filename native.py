import sys
from lexer import is_list, Symbol

def expr_to_str(expr):
    if is_list(expr):
        return '(' + ' '.join(expr_to_str(token) for token in expr) + ')'

    return str(expr)

def fn_display(expr):
    print expr_to_str(expr),

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

    'car': lambda lst: lst[0],
    'cdr': lambda lst: lst[1:],
    'cons': lambda x, lst: [x] + list(lst),

    'null?': lambda x: not x,

    'string-concatenate': fn_concat,

    'number->string': str,
    'symbol->string': lambda symbol: symbol.name,
    'string->symbol': lambda name: Symbol(name),

    'display': fn_display,
    'newline': lambda: sys.stdout.write("\n")
}
