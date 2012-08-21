def fn_print(*args):
    print ', '.join(str(arg) for arg in args)

functions = {
    'print': fn_print,
    'if': lambda cond, a, b: a if cond else b,
    '>': lambda a, b: a > b,
    '>=': lambda a, b: a >= b,
    '<': lambda a, b: a < b,
    '<=': lambda a, b: a <= b,
    'eq': lambda a, b: a == b
}
