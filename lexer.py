import re

class Token:

    def __init__(self, type_name, value):
        self.type = type_name
        self.value = value

    def __repr__(self):
        return str(self.value)

class Lexer:
    
    def __init__(self, fname):
        self.fname = fname

        self.tokens = []

        self.token_types = (
            ('float', float, re.compile('((0|[1-9]+[0-9]*)\.[0-9]+)')),
            ('int', int, re.compile('([1-9]+[0-9]*)')),
            ('str', str, re.compile('"([^"]*)"')),
            ('symbol', None, re.compile('([a-zA-Z<>=!?\+\-\*\/]+)'))
        )

    def get_tokens(self):
	line_num = 0

	for line in open(self.fname).read().splitlines():
            line_num += 1
            self.tokenize(line, line_num)

        if '(' == line:
            self.parens += 1

        if ')' == line:
            self.parens -= 1

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
        for type, cast, pattern in self.token_types:
            r = pattern.match(line);
            if not r:
                continue

            value = r.group(1)
            if cast:
                value = cast(value)

            self.tokens.append(Token(type, value))

            return line[len(r.group(0)):]

        return None
