import re

class Token:

    def __init__(self, type, value):
        if 'number' == type:
            value = int(value)

        self.type = type
        self.value = value

    def __repr__(self):
        return str(self.value)

class Lexer:
    
    def __init__(self, fname):
        self.fname = fname

        self.tokens = []

        self.token_types = {
            'number': re.compile('([1-9]+[0-9]*)'),
            'string': re.compile('"([^"]*)"'),
            'simbol': re.compile('([a-zA-Z<>=!?\+\-\*\/]+)'),
        }

    def get_tokens(self):
	line_num = 0

	for line in open(self.fname).read().splitlines():
            line_num += 1
            if not self.tokenize(line):
                raise Exception("Lexer error on line %d: \n%s" % (line_num, line))

        if '(' == line:
            self.parens += 1

        if ')' == line:
            self.parens -= 1

        return self.tokens

    def tokenize(self, line):
        line = line.lstrip()

        if len(line) == 0:
            return True

        r = self.find_atom(line)
        if None != r:
            return self.tokenize(r)

        r = self.find_token(line)
        if None != r:
            return self.tokenize(r)

        return False

    def find_atom(self, line):
        for atom in ['(', ')']:
            if line.startswith(atom):
                self.tokens.append(atom)
                return line[len(atom):]

        return None

    def find_token(self, line):
        for type, pattern in self.token_types.items():
            r = pattern.match(line);
            if not r:
                continue

            self.tokens.append(Token(type, r.group(1)))

            return line[len(r.group(0)):]

        return None
