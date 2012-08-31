import sys
from lexer import Lexer, Symbol

class Scope:

    def __init__(self, parent):
        self.vars = {}
        self.parent_scope = parent

    def define(self, symbol, value):
        self.vars[symbol.name] = value

    def bind(self, symbol, value, token):
        if is_list(token):
            return [self.bind(symbol, value, t) for t in token]

        if not is_symbol(token):
            return token

        if token.name == symbol.name:
            return value

        return token

    def eval(self, thing):
        if not thing:
            return thing

        if is_list(thing):
            if is_symbol(thing[0]):
                value = thing[0].name

                if value == 'define':
                    return self.define(thing[1], self.eval(thing[2]))

                if value in forms_special:
                    return forms_special[value](self, *thing[1:])

                if value in forms_native:
                    return forms_native_call(self, value, thing[1:])

                if value in self.vars:
                    fn = self.vars[value]

                    if not isinstance(fn, Lambda):
                        raise Exception("'%s' is not callable" % value)

                    return self.call(fn, thing[1:])

                raise Exception("Undefined procedure: '%s'" % value)
            else:
                return [self.eval(arg) for arg in thing]

        if is_symbol(thing):
            if thing.name in self.vars:
                return self.vars[thing.name]
            else:
                raise Exception("Unbound variable: '%s'." % thing.name)

        return thing

    def call(self, fn, args):
        body = fn.body

        i = 0
        for formal_arg in fn.args:
            body = self.bind(formal_arg, self.eval(args[i]), body)
            i += 1

        return self.eval(body)[-1]    # return value from last statement

class Lambda:

    def __init__(self, args, body):
        self.args = args
        self.body = body

    def __repr__(self):
        return str(self.body)

def special_if(scope, cond, a, b):
    if scope.eval(cond):
        return scope.eval(a)

    return scope.eval(b)

def special_quote(scope, expr):
    return expr

def special_lambda(scope, args, *body):
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

def forms_native_call(scope, name, args):
    evald_args = [scope.eval(arg) for arg in args]   # evaluate args before function body

    return forms_native[name](*evald_args)

def _find_forms(prefix, container):
    for key, value in globals().items():
        if key.startswith(prefix):
            container[ key[len(prefix):] ] = value

forms_special = {}
_find_forms('special_', forms_special)

def execute(fname):
    lexer = Lexer(fname)

    ast = lexer.get_ast(lexer.get_tokens())

    global_scope = Scope(None)

    return global_scope.eval(ast)

if __name__=="__main__":
    execute(sys.argv[1])
