################################################
#                                              #
#  LEXER                                       #
#                                              #
################################################

# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis

from .keywords import *
from .token import *


class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0  # self.pos is an index into self.text
        self.current_char = self.text[self.pos]
        self.mode = None

    def error(self):
        raise Exception('Invalid character')

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    # get next char
    def advance(self):
        """Advance the 'pos' pointer and set the 'current_char' variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    # skip whitespaces for next token
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def _id(self):
        """Handle identifiers and reserved keywords"""
        result = ''
        while self.current_char is not None and (
                self.current_char.isalnum() or
                self.current_char.isdigit()
                ):
            result += self.current_char
            self.advance()

        token = RESERVED_KEYWORDS.get(result, Token(KeyWords.ID, result))
        return token

    def integer(self):
        """Return a (multidigit) integer consumed from the input."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def string(self):
        """Return string consumed from the input."""
        result = ""
        self.advance()
        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            self.advance()
        self.advance()
        return result

    def array(self):
        result = []
        temp = ""
        self.advance()
        while self.current_char is not None and self.current_char != ']':
            result.append(self.integer())
            self.skip_whitespace()
            if self.current_char == ',':
                self.advance()
                self.skip_whitespace()
        self.advance()
        return result

    def comment(self):
        self.advance()
        self.advance()
        while self.current_char != '\n':
            self.advance()

    # HTML
    def html(self):
        result = ""
        while self.current_char is not None and (
                self.current_char.isalnum() or
                self.current_char == '!' or
                self.current_char == '/'
                ):
            result += self.current_char
            self.advance()

        token = RESERVED_KEYWORDS_HTML.get(result)

        if token is None:
            while self.current_char is not None and self.current_char != '<':
                result += self.current_char
                self.advance()
            token = Token(KeyWords.HTML_VALUE, result)

        return token

    def get_next_token(self):
        """Lexical analyzer (aka scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens.
        """
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == '/' and self.peek() == '/':
                self.comment()
                return self.get_next_token()

            if self.current_char.isalpha():
                return self._id()

            if self.current_char.isdigit():
                return Token(KeyWords.INTEGER, self.integer())

            if self.current_char == '+':
                self.advance()
                return Token(KeyWords.PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(KeyWords.MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(KeyWords.MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(KeyWords.DIV, '/')

            if self.current_char == '<':
                self.advance()
                return Token(KeyWords.LESS, '<')

            if self.current_char == '>':
                self.advance()
                return Token(KeyWords.GREATER, '>')

            if self.current_char == '=' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(KeyWords.EQUAL, '==')

            if self.current_char == '(':
                self.advance()
                return Token(KeyWords.LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(KeyWords.RPAREN, ')')

            if self.current_char == '=':
                self.advance()
                return Token(KeyWords.ASSIGN, '=')

            if self.current_char == ';':
                self.advance()
                return Token(KeyWords.SEMI, ';')

            if self.current_char == '"':
                return Token(KeyWords.STRING, self.string())

            if self.current_char == '[':
                # return Token(KeyWords.ARRAY, self.array())
                self.advance()
                return Token(KeyWords.LBRACK, '[')

            if self.current_char == ']':
                self.advance()
                return Token(KeyWords.RBRACK, ']')

            if self.current_char == ',':
                self.advance()
                return Token(KeyWords.COMMA, ',')

            if self.current_char == '{':
                self.advance()
                return Token(KeyWords.LBRACE, '{')

            if self.current_char == '}':
                self.advance()
                return Token(KeyWords.RBRACE, '}')

            self.error()

        return Token(KeyWords.EOF, None)
