import core, lexer
import readline

def start():
    scope = core.GlobalScope()

    while True:
        try:
            line = raw_input("scheme> ")
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
