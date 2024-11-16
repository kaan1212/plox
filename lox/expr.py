from abc import ABC, abstractmethod


class Expr(ABC):
    @abstractmethod
    def accept(self, visitor): pass


class Visitor(ABC):
    @abstractmethod
    def visitbinaryexpr(self, expr): pass
    @abstractmethod
    def visitgroupingexpr(self, expr): pass
    @abstractmethod
    def visitliteralexpr(self, expr): pass
    @abstractmethod
    def visitunaryexpr(self, expr): pass
    @abstractmethod
    def visitvariableexpr(self, expr): pass


class Binary(Expr):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visitbinaryexpr(self)


class Grouping(Expr):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visitgroupingexpr(self)


class Literal(Expr):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visitliteralexpr(self)


class Unary(Expr):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visitunaryexpr(self)


class Variable(Expr):
    def __init__(self, name):
        self.name = name

    def accept(self, visitor):
        return visitor.visitvariableexpr(self)
