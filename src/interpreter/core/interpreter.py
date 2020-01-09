################################################
#                                              #
#  INTERPRETER                                 #
#                                              #
################################################

# from Parser import *
from .lexer.keywords import *


class ExceptionType(Exception):
    def __init__(self, text):
        self.message = text


class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
        self.GLOBAL_SCOPE = {}

    def error_Type(self):
        raise Exception('No visit_{} method'.format(type(node).__name__))

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_UnaryOp(self, node):
        """
        unary operation: '+', '-'
        """
        if node.op.type == KeyWords.PLUS:
            return +self.visit(node.expr)
        elif node.op.type == KeyWords.MINUS:
            return -self.visit(node.expr)

    def visit_BinOp(self, node):
        """
        binary operation: '+', '-', '*', '/', '>', '<', '=='
        """
        if node.op.type == KeyWords.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == KeyWords.MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == KeyWords.MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == KeyWords.DIV:
            return self.visit(node.left) / self.visit(node.right)
        ################################
        elif node.op.type == KeyWords.GREATER:
            return self.visit(node.left) > self.visit(node.right)
        elif node.op.type == KeyWords.LESS:
            return self.visit(node.left) < self.visit(node.right)
        elif node.op.type == KeyWords.EQUAL:
            return self.visit(node.left) == self.visit(node.right)

    def visit_Assign(self, node):
        """
        assign: '='
        """
        var_name = node.left.value
        right = self.visit(node.right)
        var_type = node.left.var_type

        if var_type == KeyWords.NUM:
            if type(right) == int or type(right) == float:
                self.GLOBAL_SCOPE[var_name] = right
            else:
                raise(ExceptionType("Type Erorr"))
                print('ERROR NUM - ')
        elif var_type == KeyWords.STR:
            if type(right) == str:
                self.GLOBAL_SCOPE[var_name] = right
            else:
                raise(ExceptionType("Type Erorr"))
                print('ERROR STR - ')
        elif var_type == KeyWords.ARR:
            if type(right) == list:
                self.GLOBAL_SCOPE[var_name] = right
            else:
                raise(ExceptionType("Type Erorr"))
                print('ERROR LIST - ')

    def visit_Var(self, node):
        var_name = node.value
        val = self.GLOBAL_SCOPE.get(var_name)
        if val is None:
            raise NameError(repr(var_name))
        else:
            return val

    def visit_Num(self, node):
        return float(node.value)

    def visit_String(self, node):
        return node.value

    def visit_Array(self, node):
        result = []
        for item in node.items:
            result.append(self.visit(item))
        return result

    def visit_Array_Index(self, node):
        array = self.visit(node.array)
        index = int(self.visit(node.index))
        return array[index]

    def visit_Print(self, node):
        print(self.visit(node.value))

    def visit_Cond(self, node):
        """
        condition: cond | cond / else
        """
        if self.visit(node.cond) is True:
            self.visit(node.body_cond)
        else:
            self.visit(node.body_else)

    def visit_Verchu(self, node):
        """
        loop: verchu
        """
        while self.visit(node.cond) is True:
            self.visit(node.body_cond)

    def visit_Do_Verchu(self, node):
        """
        loop: do / verchu
        """
        self.visit(node.body_cond)
        while self.visit(node.cond) is True:
            self.visit(node.body_cond)

    def visit_NoOp(self, node):
        pass

    def interpret(self):
        tree = self.parser.parse()
        self.visit(tree)
