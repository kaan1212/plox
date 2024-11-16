from abc import ABC, abstractmethod


class Stmt(ABC):
    @abstractmethod
    def accept(self, visitor): pass


class Visitor(ABC):
    @abstractmethod
    def visitexpressionstmt(self, stmt): pass
    @abstractmethod
    def visitprintstmt(self, stmt): pass
    @abstractmethod
    def visitvarstmt(self, stmt): pass


class Expression(Stmt):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visitexpressionstmt(self)


class Print(Stmt):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visitprintstmt(self)


class Var(Stmt):
    def __init__(self, name, initializer):
        self.name = name
        self.initializer = initializer

    def accept(self, visitor):
        return visitor.visitvarstmt(self)
