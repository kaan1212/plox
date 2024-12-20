from lox.tokentype import TokenType
from lox.expr import *
import lox.stmt as stmt


class Parser:
    def __init__(self, tokens, logerror):
        self.tokens = tokens
        self.logerror = logerror

        self.current = 0

    def parse(self):
        # try:
        #     return self.expression()
        # except ParseError:
        #     return None

        statements = []
        while not self.isatend():
            statements.append(self.declaration())

        return statements

    def expression(self):
        return self.equality()

    def declaration(self):
        try:
            if self.match(TokenType.VAR):
                return self.vardeclaration()

            return self.statement()
        except ParseError as error:
            self.synchronize()
            return None

    def statement(self):
        if self.match(TokenType.PRINT):
            return self.printstatement()

        return self.expressionstatement()

    def printstatement(self):
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return stmt.Print(value)

    def vardeclaration(self):
        name = self.consume(TokenType.IDENTIFIER, 'Expect variable name.')

        initializer = None
        if self.match(TokenType.EQUAL):
            initializer = self.expression()

        self.consume(TokenType.SEMICOLON,
                     "Expect ';' after variable declaration.")
        return stmt.Var(name, initializer)

    def expressionstatement(self):
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return stmt.Expression(expr)

    def equality(self):
        expr = self.comparison()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)

        return expr

    def comparison(self):
        expr = self.term()

        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)

        return expr

    def term(self):
        expr = self.factor()

        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)

        return expr

    def factor(self):
        expr = self.unary()

        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)

        return expr

    def unary(self):
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)

        return self.primary()

    def primary(self):
        if self.match(TokenType.FALSE):
            return Literal(False)
        if self.match(TokenType.TRUE):
            return Literal(True)
        if self.match(TokenType.NIL):
            return Literal(None)

        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)

        if self.match(TokenType.IDENTIFIER):
            return Variable(self.previous())

        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)

        raise self.error(self.peek(), 'Expect expression.')

    def match(self, *types):
        for type in types:
            if self.check(type):
                self.advance()
                return True

        return False

    def consume(self, type, message):
        if self.check(type):
            return self.advance()

        raise self.error(self.peek(), message)

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

    def error(self, token, message):
        self.logerror(token, message)
        return ParseError()

    def synchronize(self):
        self.advance()

        while not self.isatend():
            if self.previous().type == TokenType.SEMICOLON:
                return

            match self.peek().type:
                case TokenType.CLASS | TokenType.FUN | TokenType.VAR | TokenType.FOR | TokenType.IF | TokenType.WHILE | TokenType.PRINT | TokenType.RETURN: return

            self.advance()


class ParseError(BaseException):
    pass
