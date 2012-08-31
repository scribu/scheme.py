import sys, native
from lexer import Lexer, Symbol

def is_list(token):
    return type(token) in [list, tuple]

def is_symbol(token):
    return isinstance(token, Symbol)

class Lambda:

    def __init__(self, args, body, scope):
        self.args = args
        self.body = body
        self.scope = scope

    def __repr__(self):
        return '(lambda (%s) %s)' % (
                ' '.join(str(arg) for arg in self.args),
                ' '.join(str(line) for line in self.body))

    def call(self, args):
        i = 0
        for formal_arg in self.args:
            # all formal args are bound on each call
            if len(args) <= i:
                raise Exception("Missing parameter '%s'" % formal_arg.name)

            self.scope.bind(formal_arg, args[i])
            i += 1

        # return value from last statement
        return [self.scope.eval(stmt) for stmt in self.body][-1]

class NativeLambda(Lambda):

    def __init__(self, body):
        self.body = body

    def __repr__(self):
        return '<native-code>'

    def call(self, args):
        return self.body(*args)

class Scope:

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
        if not token:
            return token

        if is_list(token):
            if is_list(token[0]):
                return [self.eval(arg) for arg in token]

            symbol = token[0]

            if symbol.name == 'quote':
                return token[1]

            if symbol.name == 'define':
                try:
                    value = self.eval(token[2])
                except IndexError:
                    value = None

                return self.bind(token[1], value)

            if symbol.name == 'set!':
                if token[1].name not in self.vars:
                    raise Exception("Unboud variable: '%s'" % token[1].name)

                return self.bind(token[1], self.eval(token[2]))

            if symbol.name == 'lambda':
                return self.make_lambda(token[1], token[2:])

            if symbol.name == 'if':
                return self.eval_if(*token[1:])

            fn = self.deref(symbol)

            try:
                return fn.call([self.eval(arg) for arg in token[1:]])
            except AttributeError:
                raise Exception("'%s' is not callable" % symbol.name)

        if is_symbol(token):
            return self.deref(token)

        return token

    def eval_if(self, cond, a, b):
        if self.eval(cond):
            return self.eval(a)

        return self.eval(b)

    def make_lambda(self, args, body):
        for arg in args:
            if not is_symbol(arg):
                raise Exception("Syntax error: '%s' is not a valid arg name" % arg)

        return Lambda(args, body, self)

class GlobalScope(Scope):

    def __init__(self):
        self.parent = None

        self.vars = { key: NativeLambda(value)
            for key, value in native.forms.items() }

def execute(fname):
    lexer = Lexer(fname)

    ast = lexer.get_ast(lexer.get_tokens())

    return GlobalScope().eval(ast)

if __name__=="__main__":
    execute(sys.argv[1])
