from lox.token import Token
from lox.tokentype import TokenType


class Scanner:
    __keywords = {
        'and':      TokenType.AND,
        'class':    TokenType.CLASS,
        'else':     TokenType.ELSE,
        'false':    TokenType.FALSE,
        'for':      TokenType.FOR,
        'fun':      TokenType.FUN,
        'if':       TokenType.IF,
        'nil':      TokenType.NIL,
        'or':       TokenType.OR,
        'print':    TokenType.PRINT,
        'return':   TokenType.RETURN,
        'super':    TokenType.SUPER,
        'this':     TokenType.THIS,
        'true':     TokenType.TRUE,
        'var':      TokenType.VAR,
        'while':    TokenType.WHILE
    }

    def __init__(self, source, error):
        self.source = source
        self.error = error

        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1

    def scantokens(self):
        while not self.__eof():
            # We are at the beginning of the next lexeme.
            self.start = self.current
            self.__scantoken()

        self.tokens.append(Token(TokenType.EOF, '', None, self.line))
        return self.tokens

    def __scantoken(self):
        c = self.__advance()
        match c:
            case '(': self.__addtoken(TokenType.LEFT_PAREN)
            case ')': self.__addtoken(TokenType.RIGHT_PAREN)
            case '{': self.__addtoken(TokenType.LEFT_BRACE)
            case '}': self.__addtoken(TokenType.RIGHT_BRACE)
            case ',': self.__addtoken(TokenType.COMMA)
            case '.': self.__addtoken(TokenType.DOT)
            case '-': self.__addtoken(TokenType.MINUS)
            case '+': self.__addtoken(TokenType.PLUS)
            case ';': self.__addtoken(TokenType.SEMICOLON)
            case '*': self.__addtoken(TokenType.STAR)
            case '!': self.__addtoken(TokenType.BANG_EQUAL if self.__match('=') else TokenType.BANG)
            case '=': self.__addtoken(TokenType.EQUAL_EQUAL if self.__match('=') else TokenType.EQUAL)
            case '<': self.__addtoken(TokenType.LESS_EQUAL if self.__match('=') else TokenType.LESS)
            case '>': self.__addtoken(TokenType.GREATER_EQUAL if self.__match('=') else TokenType.GREATER)
            case '/':
                if (self.__match('/')):
                    # A comment goes until the end of the line.
                    while self.__peek() != '\n' and not self.__eof():
                        self.__advance()
                else:
                    self.__addtoken(TokenType.SLASH)

            case ' ' | '\r' | '\t': pass  # Ignore whitespace.

            case '\n': self.line += 1

            case '"': self.__string()

            case _:
                if self.__isdigit(c):
                    self.__number()
                elif self.__isalpha(c):
                    self.__identifier()
                else:
                    self.error(self.line, 'Unexpected character.')

    def __identifier(self):
        while self.__isalphanumeric(self.__peek()):
            self.__advance()

        text = self.source[self.start: self.current]
        type = Scanner.__keywords.get(text)
        if not type:
            type = TokenType.IDENTIFIER
        self.__addtoken(type)

    def __number(self):
        while self.__isdigit(self.__peek()):
            self.__advance()

        # Look for a fractional part.
        if self.__peek() == '.' and self.__isdigit(self.__peeknext()):
            # Consume the "."
            self.__advance()

            while self.__isdigit(self.__peek()):
                self.__advance()

        self.__addtoken(TokenType.NUMBER, float(
            self.source[self.start: self.current]))

    def __string(self):
        while self.__peek() != '"' and not self.__eof():
            if self.__peek() == '\n':
                self.line += 1
            self.__advance()

        if self.__eof():
            self.error(self.line, 'Unterminated string.')
            return

        # The closing ".
        self.__advance()

        # Trim the surrounding quotes.
        value = self.source[self.start + 1: self.current - 1]
        self.__addtoken(TokenType.STRING, value)

    def __match(self, expected):
        if self.__eof():
            return False
        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def __peek(self):
        if self.__eof():
            return '\0'
        return self.source[self.current]

    def __peeknext(self):
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def __isalpha(self, c):
        c = ord(c)

        return ord('a') <= c <= ord('z') \
            or ord('A') <= c <= ord('Z') \
            or c == ord('_')

    def __isalphanumeric(self, c):
        return self.__isalpha(c) or self.__isdigit(c)

    def __isdigit(self, c):
        return ord('0') <= ord(c) <= ord('9')

    def __eof(self):
        return self.current >= len(self.source)

    def __advance(self):
        c = self.source[self.current]
        self.current += 1
        return c

    def __addtoken(self, type, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))
