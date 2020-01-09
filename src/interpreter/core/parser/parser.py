################################################
#                                              #
#  PARSER                                      #
#                                              #
################################################

from ..lexer.keywords import *
from .ast_nodes import *


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.current_token = self.lexer.get_next_token()
        self.var_type = {}

    def error(self):
        raise Exception('Error parsing input')

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def program(self):
        """
        program : statemen_list
                    | parse_html
        """
        nodes = self.statement_list()
        root = Compound()

        for node in nodes:
            root.children.append(node)
        return root

    def statement_list(self):
        """
        statement_list : statement
                    | statement SEMI statement_list
        """
        node = self.statement()

        results = [node]

        while self.current_token.type == KeyWords.SEMI:
            self.eat(KeyWords.SEMI)
            results.append(self.statement())

        if self.current_token.type == KeyWords.ID:
            self.error()

        return results

    def statement(self):
        """
        statement : declaration
                    | assignment_statement
                    | function
                    | condiion
                    | verchu
                    | do_verchu
                    | empty
        """
        # if self.current_token.type == BEGIN:
        #    node = self.compound_statement()
        if self.current_token.type == KeyWords.NUM:
            node = self.declaration()
        elif self.current_token.type == KeyWords.STR:
            node = self.declaration()
        elif self.current_token.type == KeyWords.ARR:
            node = self.declaration()
        elif self.current_token.type == KeyWords.ID:
            node = self.assignment_statement()
        elif self.current_token.type == KeyWords.PRINT:
            node = self.function()
        elif self.current_token.type == KeyWords.COND:
            node = self.condition()
        elif self.current_token.type == KeyWords.VERCHU:
            node = self.loop_verchu()
        elif self.current_token.type == KeyWords.DO:
            node = self.loop_do_verchu()
        else:
            node = self.empty()
        return node

    def declaration(self):
        """
        declare type of variable
        declaration: (NUM | STR | ARR) assignment_statement
        """
        token = self.current_token
        if token.type == KeyWords.NUM:
            self.eat(KeyWords.NUM)
            self.var_type[self.current_token.value] = KeyWords.NUM
        elif token.type == KeyWords.STR:
            self.eat(KeyWords.STR)
            self.var_type[self.current_token.value] = KeyWords.STR
        elif token.type == KeyWords.ARR:
            self.eat(KeyWords.ARR)
            self.var_type[self.current_token.value] = KeyWords.ARR
        return self.assignment_statement()

    def function(self):
        """
        function: print
        """
        if self.current_token.type == KeyWords.PRINT:
            return self.print()

    def print(self):
        """
        print: PRINT expr
        """
        token = self.current_token
        self.eat(KeyWords.PRINT)
        right = self.expr()
        node = Print(token, right)
        return node

    def assignment_statement(self):
        """
        assignment_statement : variable ASSIGN expr
        """
        left = self.variable()
        token = self.current_token
        self.eat(KeyWords.ASSIGN)
        right = self.expr()
        node = Assign(left, token, right)
        return node

    def variable(self):
        """
        variable : ID
        """
        variable_type = self.var_type[self.current_token.value]
        node = Var(self.current_token, variable_type)
        self.eat(KeyWords.ID)
        return node

    def array(self):
        """
        array: LBRACK (expr | expr (COMMA expr)* ) RBRACK
        """
        self.eat(KeyWords.LBRACK)
        result = [self.expr()]

        while self.current_token.type == KeyWords.COMMA:
            self.eat(KeyWords.COMMA)
            result.append(self.expr())

        self.eat(KeyWords.RBRACK)
        return result

    def empty(self):
        """An empty production"""
        return NoOp()

    def factor(self):
        """
        factor : PLUS factor
                | MINUS factor
                | INTEGER
                | STRING
                | array
                | LPARAN expr RPARAN
                | variable
        """

        token = self.current_token
        if token.type == KeyWords.PLUS:
            self.eat(KeyWords.PLUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == KeyWords.MINUS:
            self.eat(KeyWords.MINUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == KeyWords.INTEGER:
            self.eat(KeyWords.INTEGER)
            return Num(token)
        elif self.current_token.type == KeyWords.STRING:
            self.eat(KeyWords.STRING)
            return String(token)
        elif self.current_token.type == KeyWords.LBRACK:
            array_elements = self.array()
            array = Array()
            for item in array_elements:
                array.items.append(item)
            return array
        elif self.current_token.type == KeyWords.LPAREN:
            self.eat(KeyWords.LPAREN)
            node = self.expr()
            self.eat(KeyWords.RPAREN)
            return node
        else:
            node = self.variable()
            return node

    def term(self):
        """
        term   : factor((MUL | DIV) factor) *
                | LBRACK expr RBRACK
        """
        node = self.factor()

        while self.current_token.type in (KeyWords.MUL, KeyWords.DIV):
            token = self.current_token
            if token.type == KeyWords.MUL:
                self.eat(KeyWords.MUL)
            elif token.type == KeyWords.DIV:
                self.eat(KeyWords.DIV)

            node = BinOp(left=node, op=token, right=self.factor())

        if self.current_token.type == KeyWords.LBRACK:
            self.eat(KeyWords.LBRACK)
            index = self.expr()
            self.eat(KeyWords.RBRACK)
            # якщо b = 3 * a[1] буде BinOp(3, *, a)
            # я поміняю на BinOp(3, *, Array_Index(a, 1))
            if type(node) == BinOp:
                node.right = Array_Index(node.right, index)
            else:
                return Array_Index(node, index)

        return node

    def expr(self):
        """
        expr   : term((PLUS | MINUS) term)  *
                | term (GREATER | LESS | EQUAL) expr
        """
        node = self.term()

        while self.current_token.type in (KeyWords.PLUS, KeyWords.MINUS):
            token = self.current_token
            if token.type == KeyWords.PLUS:
                self.eat(KeyWords.PLUS)
            elif token.type == KeyWords.MINUS:
                self.eat(KeyWords.MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        token = self.current_token
        if token.type == KeyWords.GREATER:
            self.eat(KeyWords.GREATER)
        elif token.type == KeyWords.LESS:
            self.eat(KeyWords.LESS)
        elif token.type == KeyWords.EQUAL:
            self.eat(KeyWords.EQUAL)

        if token.type in (KeyWords.GREATER, KeyWords.LESS, KeyWords.EQUAL):
            node = BinOp(left=node, op=token, right=self.expr())

        return node

    def condition(self):
        """
        condition : COND expr LBRACE program RBRACE
                    (empty | ELSE LBRACE program RBRACE)
        """
        self.eat(KeyWords.COND)
        cond = self.expr()
        self.eat(KeyWords.LBRACE)
        body_cond = self.program()
        self.eat(KeyWords.RBRACE)

        if self.current_token.type == KeyWords.ELSE:
            self.eat(KeyWords.ELSE)
            self.eat(KeyWords.LBRACE)
            body_else = self.program()
            self.eat(KeyWords.RBRACE)
            return Cond(cond, body_cond, body_else)

        return Cond(cond, body_cond, NoOp())

    def loop_verchu(self):
        """
        verchu    : VERCHU expr LBRACE program RBRACE
        """
        self.eat(KeyWords.VERCHU)
        cond = self.expr()
        self.eat(KeyWords.LBRACE)
        body_cond = self.program()
        self.eat(KeyWords.RBRACE)

        return Verchu(cond, body_cond)

    def loop_do_verchu(self):
        """
        do_verchu : DO LBRACE program RBRACE VERCHU expr
        """
        self.eat(KeyWords.DO)
        self.eat(KeyWords.LBRACE)
        body_cond = self.program()
        self.eat(KeyWords.RBRACE)
        self.eat(KeyWords.VERCHU)
        cond = self.expr()

        return Do_Verchu(cond, body_cond)

    def parse(self):
        node = self.program()
        return node
