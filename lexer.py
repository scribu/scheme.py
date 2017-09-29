"""The lexer is the component which converts a source code string into a list of tokens and then to an AST."""
import re
from collections import defaultdict


class Symbol:
    """A symbol is a special token, representing a variable."""

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return str(self.name)


def is_symbol(token):
    return isinstance(token, Symbol)


def is_list(token):
    return type(token) in [list, tuple]


def convert_bool(value):
    return True if '#t' == value else False


TOKEN_TYPES = (
    (convert_bool, re.compile('(#[tf])')),
    (float, re.compile('((0|[1-9]+[0-9]*)\.[0-9]+)')),
    (int, re.compile('(0|[1-9]+[0-9]*)')),
    (str, re.compile('"([^"]*)"')),
    (Symbol, re.compile('([^\(\)\'"\s]+)'))
)


def _find_atom(line, tokens):
    if line.startswith(';'):
        return ''

    for atom in ['(', ')', "'"]:
        if line.startswith(atom):
            tokens.append(atom)
            return line[len(atom):]

    return None


def _find_token(line, tokens):
    for cast, pattern in TOKEN_TYPES:
        r = pattern.match(line);
        if not r:
            continue

        tokens.append(cast(r.group(1)))

        return line[len(r.group(0)):]

    return None


def _tokenize(line, tokens):
    line = line.lstrip()

    if len(line) == 0:
        return

    r = _find_atom(line, tokens)
    if None != r:
        _tokenize(r, tokens)
        return

    r = _find_token(line, tokens)
    if None != r:
        _tokenize(r, tokens)
        return

    raise Exception("Failed tokenizing: %s" % line)


def tokenize(line):
    tokens = []
    _tokenize(line, tokens)
    return tokens


def tokenize_file(fname):
    line_num = 0

    tokens = []

    for line in open(fname).read().splitlines():
        line_num += 1

        try:
            _tokenize(line, tokens)
        except:
            raise Exception("Lexer error on line %d: \n%s" % (line_num, line))

    return tokens


def get_ast(tokens):
    """
    Transform flat token list into a tree.
    """

    lists = defaultdict(list)

    i = 0
    level = 0

    while i < len(tokens):
        if '(' == tokens[i]:
            level += 1
        elif ')' == tokens[i]:
            lists[level-1].append(lists[level])
            del(lists[level])
            level -= 1
        else:
            lists[level].append(tokens[i])

        i += 1

    return (lists[0], level)


def expand_quotes(expr):
    """
    Converts '(1 2 3) to (quote (1 2 3))
    """

    if not is_list(expr):
        return expr

    new_expr = []

    n = len(expr)

    i = 0
    while i<n:
        if "'" == expr[i]:
            new_expr.append([Symbol('quote'), expand_quotes(expr[i+1])])
            i += 2
        else:
            new_expr.append(expand_quotes(expr[i]))
            i += 1

    return new_expr


def expand_define(expr):
    """
    Converts (define (fn x) ...) to (define fn (lambda (x) ...))
    """

    if not is_list(expr):
        return expr

    new_expr = []

    n = len(expr)

    i = 0
    while i<n:
        if is_symbol(expr[i]) and expr[i].name == 'define' and is_list(expr[i+1]):
            symbol, args = expr[i+1][0], expr[i+1][1:]
            body = expand_define(expr[i+2:])

            new_expr += [expr[i], symbol, [Symbol('lambda'), args] + body]
            break
        else:
            new_expr.append(expand_define(expr[i]))
            i += 1

    return new_expr


def expr_to_str(expr):
    if is_list(expr):
        return '(' + ' '.join(expr_to_str(token) for token in expr) + ')'

    if bool == type(expr):
        return '#t' if expr else '#f'

    return str(expr)
