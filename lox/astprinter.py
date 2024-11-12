from lox.expr import *
from lox.token import Token
from lox.tokentype import TokenType


class AstPrinter(Visitor):
    def print(self, expr):
        return expr.accept(self)

    def visitbinaryexpr(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visitgroupingexpr(self, expr):
        return self.parenthesize('group', expr.expression)

    def visitliteralexpr(self, expr):
        if expr.value == None:
            return 'nil'
        return str(expr.value)

    def visitunaryexpr(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def parenthesize(self, name, *exprs):
        # See: https://www.python.org/doc/essays/list2str/
        builder = ''

        builder += '(' + name
        for expr in exprs:
            builder += ' '
            builder += expr.accept(self)
        builder += ')'

        return builder


# "You can go ahead and delete this method."
def main():
    expression = Binary(
        Unary(
            Token(TokenType.MINUS, '-', None, 1),
            Literal(123)
        ),
        Token(TokenType.STAR, '*', None, 1),
        Grouping(
            Literal(45.67)
        )
    )

    print(AstPrinter().print(expression))


if __name__ == '__main__':
    main()
