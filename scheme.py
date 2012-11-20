import sys

def execute_file(fname):
    import core, lexer

    scope = core.GlobalScope()

    ast, balance = lexer.get_ast(lexer.tokenize_file(fname))

    if balance != 0:
        raise Exception("Unbalanced parentheses")

    for expr in ast:
        scope.eval(expr)

def main():
    if len(sys.argv) > 1:
        execute_file(sys.argv[1])
    else:
        from repl import REPL
        REPL().start()

if __name__=="__main__":
    main()
