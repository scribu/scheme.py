"""The entry point to the interpreter."""
import sys

if len(sys.argv) > 1:
    import core

    core.proc_load(core.GlobalScope(), sys.argv[1])
else:
    from repl import REPL
    REPL().start()
