from lox.environment import Environment
from lox.expr import Visitor
from lox.tokentype import TokenType


class Interpreter(Visitor):
    def __init__(self, runtimeerror):
        self.runtimeerror = runtimeerror
        self.environment = Environment()

    # def interpret(self, expression):
    #     try:
    #         value = self.evaluate(expression)
    #         print(self.stringify(value))
    #     except RuntimeError as error:
    #         # todo: Create own exception class like in the book.
    #         self.runtimeerror(error)

    def interpret(self, statements):
        try:
            for statement in statements:
                self.execute(statement)
        except RuntimeError as error:
            self.runtimeerror(error)

    def visitliteralexpr(self, expr):
        return expr.value

    def visitunaryexpr(self, expr):
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case TokenType.BANG:
                return not self.istruthy(right)
            case TokenType.MINUS:
                self.checknumberoperand(expr.operator, right)
                return -right

        # Unreachable.
        return None

    def visitvariableexpr(self, expr):
        return self.environment.get(expr.name)

    def checknumberoperand(self, operator, operand):
        if isinstance(operand, float):
            return
        raise RuntimeError(operator, 'Operand must be a number.')

    def checknumberoperands(self, operator, left, right):
        if isinstance(left, float) and isinstance(right, float):
            return

        raise RuntimeError(operator, 'Operands must be numbers.')

    def istruthy(self, object):
        if object == None:
            return False
        if isinstance(object, bool):
            return object  # todo: Check this.
        return True

    def isequal(self, a, b):
        if a == None and b == None:
            return True
        if a == None:
            return False

        # todo: Check if this behaves like in Java.
        return a == b

    def stringify(self, object):
        if object == None:
            return 'nil'

        if isinstance(object, float):
            text = str(object)
            if text.endswith('.0'):
                text = text[:-2]
            return text

        # Added by me.
        if isinstance(object, bool):
            return str(object).lower()

        return str(object)

    def visitgroupingexpr(self, expr):
        return self.evaluate(expr.expression)

    def evaluate(self, expr):
        return expr.accept(self)

    def execute(self, stmt):
        stmt.accept(self)

    def visitexpressionstmt(self, stmt):
        self.evaluate(stmt.expression)
        return None

    def visitprintstmt(self, stmt):
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))
        return None

    def visitvarstmt(self, stmt):
        value = None
        if stmt.initializer != None:
            value = self.evaluate(stmt.initializer)

        self.environment.define(stmt.name.lexeme, value)
        return None

    def visitbinaryexpr(self, expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case TokenType.GREATER:
                self.checknumberoperands(expr.operator, left, right)
                return left > right
            case TokenType.GREATER_EQUAL:
                self.checknumberoperands(expr.operator, left, right)
                return left >= right
            case TokenType.LESS:
                self.checknumberoperands(expr.operator, left, right)
                return left < right
            case TokenType.LESS_EQUAL:
                self.checknumberoperands(expr.operator, left, right)
                return left <= right
            case TokenType.BANG_EQUAL:
                return not self.isequal(left, right)
            case TokenType.EQUAL_EQUAL:
                return self.isequal(left, right)
            case TokenType.MINUS:
                self.checknumberoperands(expr.operator, left, right)
                return left - right
            case TokenType.PLUS:
                if isinstance(left, float) and isinstance(right, float):
                    return left + right

                if isinstance(left, str) and isinstance(right, str):
                    return left + right

                raise RuntimeError(
                    expr.operator, 'Operands must be two numbers or two strings.')
            case TokenType.SLASH:
                self.checknumberoperands(expr.operator, left, right)
                return left / right
            case TokenType.STAR:
                self.checknumberoperands(expr.operator, left, right)
                return left * right

        # Unreachable.
        return None
