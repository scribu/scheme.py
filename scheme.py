import sys

def execute_file(fname):
    import core, lexer

    scope = core.GlobalScope()

    tokens = lexer.tokenize_file(fname)
    ast, balance = lexer.get_ast(tokens)

    if balance != 0:
        raise Exception("Unbalanced parentheses")

    ast = lexer.expand_quotes(ast)

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
