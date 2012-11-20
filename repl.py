import core, lexer
import readline

def get_options(scope, name):
    known_names = core.fexpr.keys() + scope.vars.keys()

    return [var for var in known_names if var.startswith(name)]

class REPL:

    def __init__(self):
        self.scope = core.GlobalScope()

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
                tokens = lexer.tokenize(line)
            except Exception as e:
                print e
                continue

            stored_tokens += tokens

            try:
                ast = lexer.get_ast(stored_tokens)
            except Exception:
                continue

            stored_tokens = []

            for expr in ast:
                print self.scope.eval(expr)

    def completer(self, input, state):
        tokens = lexer.tokenize(input)

        symbol = tokens[-1]

        if not lexer.is_symbol(symbol):
            return None

        options = get_options(self.scope, symbol.name)

        if state >= len(options):
            return None

        tokens[-1] = options[state]

        return ''.join(tokens)

