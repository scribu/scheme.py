"""The core of the interpreter."""
from __future__ import division
from __future__ import print_function

import sys
import operator
import lexer
from lexer import Symbol, is_list, is_symbol, expr_to_str

def is_procedure(arg):
    return isinstance(arg, Lambda)


def fn_display(expr):
    print(expr_to_str(expr), end='')


def fn_concat(args):
    return ''.join(args)


def fn_list(*args):
    return args


def fn_add(*args):
    return reduce(operator.add, args, 0)


def fn_mul(*args):
    return reduce(operator.mul, args, 1)


# built-in procedures that don't need access to the current scope
functions = {
    # mathematical operators
    '+': fn_add,
    '*': fn_mul,
    '-': lambda a, b: a - b,
    '/': lambda a, b: a / b,
    '%': lambda a, b: a % b,

    # comparison operators
    '=': lambda a, b: float(a) == float(b),
    '>': lambda a, b: a > b,
    '>=': lambda a, b: a >= b,
    '<': lambda a, b: a < b,
    '<=': lambda a, b: a <= b,

    # equivalence predicates
    'eq?': lambda a, b: a is b,
    'eqv?': lambda a, b: a is b,
    'equal?': lambda a, b: a == b,

    # type predicates
    'null?': lambda x: not x,
    'boolean?': lambda x: bool == type(x),
    'string?': lambda x: str == type(x),
    'list?': is_list,
    'symbol?': is_symbol,
    'procedure?': is_procedure,

    # evaluation
    'apply': lambda fn, args: fn(args),

    # converters
    'number->string': str,
    'symbol->string': lambda symbol: symbol.name,
    'string->symbol': lambda name: Symbol(name),

    # list manipulation
    'list': fn_list,
    'car': lambda lst: lst[0],
    'cdr': lambda lst: lst[1:],
    'cons': lambda x, lst: [x] + list(lst),

    # string manipulation
    'string-concatenate': fn_concat,

    # display procedures
    'display': fn_display,
    'newline': lambda: sys.stdout.write("\n")
}

def proc_eval(scope, expr):
    """A procedure for evaluating an expression."""
    return scope.eval(expr)


def proc_load(scope, fname):
    """A procedure for loading code from a file."""
    tokens = lexer.tokenize_file(fname)
    ast, balance = lexer.get_ast(tokens)

    if balance != 0:
        raise Exception("Unbalanced parentheses")

    ast = lexer.expand_quotes(ast)
    ast = lexer.expand_define(ast)

    for expr in ast:
        scope.eval(expr)

procedures = {
    'eval': proc_eval,
    'load': proc_load,
}


def fexpr_quote(scope, expr):
    return expr


def fexpr_if(scope, cond, a, b):
    if scope.eval(cond):
        return scope.eval(a)

    return scope.eval(b)


def fexpr_begin(scope, *body):
    # return value from last statement
    return [scope.eval(stmt) for stmt in body][-1]


def fexpr_lambda(scope, args, *body):
    for arg in args:
        if not is_symbol(arg):
            raise Exception("Syntax error: '%s' is not a valid arg name" % arg)

    return Lambda(body, scope, args)


def fexpr_define(scope, symbol, *tokens):
    try:
        value = scope.eval(tokens[0])
    except IndexError:
        value = None

    return scope.bind(symbol, value)


def fexpr_set(scope, symbol, value):
    while symbol.name not in scope.vars:
        if not scope.parent:
            raise Exception("Unbound variable: '%s'" % symbol.name)

        scope = scope.parent

    return scope.bind(symbol, scope.eval(value))


# special forms that receive unevaluated args
fexpr = {
    'quote': fexpr_quote,
    'if': fexpr_if,
    'begin': fexpr_begin,
    'lambda': fexpr_lambda,
    'define': fexpr_define,
    'set!': fexpr_set
}


class Lambda:
    """A lambda is an annonymous function."""

    def __init__(self, body, scope, args):
        self.body = body
        self.scope = scope
        self.args = args

    def __repr__(self):
        return '(lambda (%s) %s)' % (
                ' '.join(expr_to_str(arg) for arg in self.args),
                ' '.join(expr_to_str(line) for line in self.body))

    def __call__(self, args):
        local_scope = Scope(self.scope)

        i = 0
        for formal_arg in self.args:
            if len(args) <= i:
                raise Exception("Missing parameter '%s'" % formal_arg.name)

            local_scope.bind(formal_arg, args[i])
            i += 1

        return fexpr_begin(local_scope, *self.body)


class NativeLambda(Lambda):
    """A lambda that's implemented in Python."""

    def __init__(self, body, scope, name):
        self.body = body
        self.scope = scope
        self.name = name

    def __repr__(self):
        return '#<procedure %s>' % self.name

    def __call__(self, args):
        return self.body(self.scope, *args)


class ScopelessNativeLambda(NativeLambda):

    def __call__(self, args):
        return self.body(*args)


class Scope:
    """A scope is the context within which an expression is evaluated."""

    def __init__(self, parent):
        self.vars = {}
        self.parent = parent

    def __repr__(self):
        vars = "\n".join('%s: %s' % (str(key), str(value))
                for key, value in self.vars.items())

        return "\n----------\n%s\n----------" % vars

    def bind(self, symbol, value):
        self.vars[symbol.name] = value

    def deref(self, symbol):
        if symbol.name in self.vars:
            return self.vars[symbol.name]

        if self.parent:
            return self.parent.deref(symbol)

        raise Exception("Unbound variable: '%s'." % symbol.name)

    def eval(self, token):
        if is_list(token):
            if not len(token):
                return token

            fn = self.eval(token[0])

            if not hasattr(fn, '__call__'):
                raise Exception("Uncallable expression: %s" % fn)

            args = token[1:]

            if is_procedure(fn):
                return fn([self.eval(arg) for arg in args])

            # special form
            return fn(self, *args)

        if is_symbol(token):
            if token.name in fexpr:
                return fexpr[token.name]

            return self.deref(token)

        return token


class GlobalScope(Scope):
    """The top-level scope, with some built-in functions."""

    def __init__(self):
        self.parent = None

        self.vars = {}

        for name, body in functions.items():
            self.vars[name] = ScopelessNativeLambda(body, self, name)

        for name, body in procedures.items():
            self.vars[name] = NativeLambda(body, self, name)
