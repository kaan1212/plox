from lox.tokentype import TokenType
from lox.expr import *


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def expression(self):
        return self.equality()

    def equality(self):
        expr = self.comparison()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)

        return expr

    def match(self, *types):
        for type in types:
            if self.check(type):
                self.advance()
                return True

        return False

    def check(self, type):
        if self.isatend():
            return False
        return self.peek().type == type

    def advance(self):
        if not self.isatend():
            self.current += 1
        return self.previous()

    def isatend(self):
        return self.peek().type == TokenType.EOF

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]
