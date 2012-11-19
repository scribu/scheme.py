import sys

def execute_file(fname):
    import core, lexer

    scope = core.GlobalScope()

    ast = lexer.get_ast(lexer.tokenize_file(fname))

    for expr in ast:
        scope.eval(expr)

def main():
    if len(sys.argv) > 1:
        execute_file(sys.argv[1])
    else:
        import repl
        repl.start()

if __name__=="__main__":
    main()
