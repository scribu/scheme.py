import sys

def execute_file(fname):
    import core
    from lexer import Lexer

    lexer = Lexer(fname)

    ast = lexer.get_ast(lexer.get_tokens())

    return core.GlobalScope().eval(ast)

def main():
    if len(sys.argv) > 1:
        execute_file(sys.argv[1])
    else:
        import repl
        repl.start()

if __name__=="__main__":
    main()
