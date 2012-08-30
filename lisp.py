from lexer import Lexer, Token
from collections import defaultdict

def fn_if(cond, a, b):
    if eval(cond):
        return eval(a)

    return eval(b)

def fn_print(*args):
    print ', '.join(str(arg) for arg in args)

def fn_concat(*args):
    return ''.join(str(arg) for arg in args)

def fn_list(*args):
    return args

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

    'list': fn_list,
    'car': lambda a: a[0],
    'cdr': lambda a: a[1:],

    'concat': fn_concat,
    'print': fn_print,
}

user_globals = {}

def is_list(token):
    return type(token) in [list, tuple]

def is_symbol(token):
    return hasattr(token, 'type') and 'symbol' == token.type

def native_fn_call(name, args):
    evald_args = [eval(arg) for arg in args]   # evaluate args before function body
    derefd_args = [token.value if hasattr(token, 'value') else token
            for token in evald_args]
    return native_fn[name](*derefd_args)

def global_def(name, value):
    user_globals[name] = eval(value)

def lambda_def(args, body):
    for arg in args:
        if not is_symbol(arg):
            raise Exception("Syntax error: '%s' is not a valid arg name" % arg)

    return Token('lambda', {
        'args': args,
        'body': body
    })

def _bind_var(name, value, token):
    if is_list(token):
        return [_bind_var(name, value, t) for t in token]

    if token.value == name.value:
        return value

    return token

def user_fn_call(name, args):
    fn = user_globals[name]

    if fn.type is not 'lambda':
        raise Exception("'%s' is not callable" % name)

    body = fn.value['body']

    i = 0
    for formal_arg in fn.value['args']:
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

def eval(lst):
    if not lst or not is_list(lst):
        return lst

    if is_symbol(lst[0]):
        value = lst[0].value

        if 'if' == value:
            return fn_if(*lst[1:])

        if 'define' == value:
            return global_def(lst[1].value, lst[2])

        if 'lambda' == value:
            return lambda_def(lst[1], lst[2:])

        if value in native_fn:
            return native_fn_call(value, lst[1:])

        if value in user_globals:
            return user_fn_call(value, lst[1:])

    return [eval(arg) for arg in lst]

# transform token list into an actual tree
def parse(tokens):
    lists = defaultdict(list)

    i = 0
    level = 0

    while i < len(tokens):
        if '(' == tokens[i]:
            level += 1
        elif ')' == tokens[i]:
            lists[level-1].append(lists[level])
            del(lists[level])
            level -= 1
        else:
            lists[level].append(tokens[i])

        i += 1

    if level > 0:
        raise Exception("Unbalanced parentheses")

    return lists[0]

def execute(fname):
    lexer = Lexer(fname)

    tokens = lexer.get_tokens()
    ast = parse(tokens)

    return eval(ast)
