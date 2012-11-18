import core, lexer

def start():
    scope = core.GlobalScope()

    while True:
        line = raw_input("scheme> ")

        try:
            ast = lexer.get_ast(lexer.tokenize(line))
            scope.eval(ast)
        except Exception as e:
            print e
