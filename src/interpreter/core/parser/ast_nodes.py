class AST(object):
    pass


class Compound(AST):
    """Represents a 'BEGIN ... END' block"""
    def __init__(self):
        self.children = []


# classes for language
class UnaryOp(AST):
    """Unary operation (-5) (+4) """
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr


class BinOp(AST):
    """Binary operation"""
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Assign(AST):
    """Assign node"""
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Var(AST):
    """The Var node is constructed out of ID token."""
    def __init__(self, token,  var_type):
        self.token = token
        self.value = token.value
        self.var_type = var_type


class Num(AST):
    """The Num node is constructed out of ID token."""
    def __init__(self, token):
        self.token = token
        self.value = token.value


class String(AST):
    """String node"""
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Array(AST):
    def __init__(self):
        self.items = []


class Array_Index(AST):
    def __init__(self, array, index):
        self.array = array
        self.index = index


class Print(AST):
    """The Var node is constructed out of ID token."""
    def __init__(self, token, right):
        self.token = token
        self.value = right


class Cond(AST):
    """ Conditional (if) """
    def __init__(self, cond, body_cond, body_else):
        self.cond = cond
        self.body_cond = body_cond
        self.body_else = body_else


class Verchu(AST):
    """ Loop (while) """
    def __init__(self, cond, body_cond):
        self.cond = cond
        self.body_cond = body_cond


class Do_Verchu(AST):
    """ Loop (do/while) """
    def __init__(self, cond, body_cond):
        self.cond = cond
        self.body_cond = body_cond


class NoOp(AST):
    pass
