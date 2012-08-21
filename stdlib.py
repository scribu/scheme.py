def fn_print(*args):
    print ', '.join(str(arg) for arg in args)

def fn_concat(*args):
    return ''.join(str(arg) for arg in args)

native_fn = {
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

    'concat': fn_concat,
    'print': fn_print,
}
