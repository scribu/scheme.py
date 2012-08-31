import re
from collections import defaultdict

class Symbol:

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)

def convert_bool(value):
    return True if 't' == value else False

class Lexer:
    
    def __init__(self, fname):
        self.fname = fname

        self.tokens = []

        self.token_types = (
            (convert_bool, re.compile('#([tf])')),
            (float, re.compile('((0|[1-9]+[0-9]*)\.[0-9]+)')),
            (int, re.compile('(0|[1-9]+[0-9]*)')),
            (str, re.compile('"([^"]*)"')),
            (Symbol, re.compile('([^\(\)\'"\s]+)'))
        )

    def get_ast(self, tokens):
        # transform token list into an actual tree
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

    def get_tokens(self):
	line_num = 0

	for line in open(self.fname).read().splitlines():
            line_num += 1
            self.tokenize(line, line_num)

        return self.tokens

    def tokenize(self, line, line_num):
        line = line.lstrip()

        if len(line) == 0:
            return True

        r = self.find_atom(line)
        if None != r:
            return self.tokenize(r, line_num)

        r = self.find_token(line)
        if None != r:
            return self.tokenize(r, line_num)

        raise Exception("Lexer error on line %d: \n%s" % (line_num, line))

    def find_atom(self, line):
        for atom in ['(', ')']:
            if line.startswith(atom):
                self.tokens.append(atom)
                return line[len(atom):]

        return None

    def find_token(self, line):
        for cast, pattern in self.token_types:
            r = pattern.match(line);
            if not r:
                continue

            self.tokens.append(cast(r.group(1)))

            return line[len(r.group(0)):]

        return None
