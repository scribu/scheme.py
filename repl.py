import core, lexer
import readline

def start():
    scope = core.GlobalScope()

    def completer(text, state):
        text = text.lstrip('(')
        options = [i for i in scope.vars.keys() if i.startswith(text)]
        if state < len(options):
            return options[state]
        else:
            return None

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
