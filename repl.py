"""A read-eval-print-loop implementation."""
from __future__ import print_function

import core, reader
import readline

class REPL:

    def __init__(self):
        self.scope = core.GlobalScope()

        self.init_history()
        self.init_completer()

    def init_history(self):
        import os, atexit

        histfile = os.path.join(os.path.expanduser("~"), ".schemepyhist")

        try:
            readline.read_history_file(histfile)
        except IOError:
            pass

        atexit.register(readline.write_history_file, histfile)

    def init_completer(self):
        readline.parse_and_bind("tab: complete")
        readline.set_completer_delims(' ')
        readline.set_completer(self.completer)

    def start(self):
        stored_tokens = []

        while True:
            try:
                line = raw_input("scheme> ").strip()
            except EOFError:
                print
                break

            if not line:
                continue

            try:
                tokens = reader.tokenize(line)
            except Exception as e:
                print(e)
                continue

            stored_tokens += tokens

            ast, balance = reader.get_ast(stored_tokens)

            if balance > 0:
                continue
            elif balance < 0:
                print('Unexpected ")"')
                stored_tokens = []
                continue

            stored_tokens = []

            ast = reader.expand_quotes(ast)
            ast = reader.expand_define(ast)

            for expr in ast:
                print(self.scope.eval(expr))

    def completer(self, input, state):
        tokens = reader.tokenize(input)

        symbol = tokens[-1]

        if not reader.is_symbol(symbol):
            return None

        options = self.get_options(self.scope, symbol.name)

        if state >= len(options):
            return None

        tokens[-1] = options[state]

        return ''.join(tokens)

    @staticmethod
    def get_options(scope, name):
        known_names = core.fexpr.keys() + scope.vars.keys()

        return [var for var in known_names if var.startswith(name)]
