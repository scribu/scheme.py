import re
from collections import defaultdict

class Symbol:

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

token_types = (
    (convert_bool, re.compile('(#[tf])')),
    (float, re.compile('((0|[1-9]+[0-9]*)\.[0-9]+)')),
    (int, re.compile('(0|[1-9]+[0-9]*)')),
    (str, re.compile('"([^"]*)"')),
    (Symbol, re.compile('([^\(\)\'"\s]+)'))
)

def find_atom(line, tokens):
    for atom in ['(', ')']:
        if line.startswith(atom):
            tokens.append(atom)
            return line[len(atom):]

    return None

def find_token(line, tokens):
    for cast, pattern in token_types:
        r = pattern.match(line);
        if not r:
            continue

        tokens.append(cast(r.group(1)))

        return line[len(r.group(0)):]

    return None

def tokenize(line):
    tokens = []
    _tokenize(line, tokens)
    return tokens

def _tokenize(line, tokens):
    line = line.lstrip()

    if len(line) == 0:
        return

    r = find_atom(line, tokens)
    if None != r:
        _tokenize(r, tokens)
        return

    r = find_token(line, tokens)
    if None != r:
        _tokenize(r, tokens)
        return

    raise Exception("Failed tokenizing: %s" % line)

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

    if level > 0:
        raise Exception("Unbalanced parentheses")

    return lists[0]

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

def expr_to_str(expr):
    if is_list(expr):
        return '(' + ' '.join(expr_to_str(token) for token in expr) + ')'

    return str(expr)

