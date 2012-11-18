import core, lexer
import readline

def get_options(scope, name):
    known_names = core.fexpr.keys() + scope.vars.keys()

    return [var for var in known_names if var.startswith(name)]

def start():
    scope = core.GlobalScope()

    def completer(input, state):
        tokens = lexer.tokenize(input)

        symbol = tokens[-1]

        if not lexer.is_symbol(symbol):
            return None

        options = get_options(scope, symbol.name)

        if state >= len(options):
            return None

        tokens[-1] = options[state]

        return ''.join(tokens)

    readline.parse_and_bind("tab: complete")
    readline.set_completer_delims(' ')
    readline.set_completer(completer)

    while True:
        try:
            line = raw_input("scheme> ")
            line = line.strip()

            if not line:
                continue

            line = '(display %s)' % line

            try:
                ast = lexer.get_ast(lexer.tokenize(line))
                scope.eval(ast)
                print
            except Exception as e:
                print e
        except EOFError:
            print
            break
