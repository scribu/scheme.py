import core, lexer

def start():
    scope = core.GlobalScope()

    while True:
        try:
            line = raw_input("scheme> ")

            try:
                ast = lexer.get_ast(lexer.tokenize(line))
                scope.eval(ast)
            except Exception as e:
                print e
        except EOFError:
            print
            break
