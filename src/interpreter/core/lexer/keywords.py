from .token import Token


# Keywords of language
class KeyWords(object):
    PLUS      = 'PLUS'
    MINUS     = 'MINUS'
    MUL       = 'MUL'
    DIV       = 'DIV'
    GREATER   = 'GREATER'
    LESS      = 'LESS'
    EQUAL     = 'EQUAL'
    LPAREN    = 'LPAREN'     # (
    RPAREN    = 'RPAREN'     # )

    ID        = 'ID'
    ASSIGN    = 'ASSIGN'
    INTEGER   = 'INTEGER'
    STRING    = 'STRING'
    # ARRAY     = 'ARRAY'
    SEMI      = 'SEMI'
    PRINT     = 'PRINT'
    LBRACK    = 'LBRACK'     # [
    RBRACK    = 'RBRACK'     # ]
    COMMA     = 'COMMA'

    COND      = 'COND'       # if
    LBRACE    = 'LBRACE'     # {
    RBRACE    = 'RBRACE'     # }
    ELSE      = 'ELSE'
    VERCHU    = 'VERCHU'     # while
    DO        = 'DO'         # do/while

    NUM       = 'NUM'
    STR       = 'STR'
    ARR       = 'ARR'

    EOF       = 'EOF'

    LANGUAGE  = 0
    HTML_WEB  = 1


# Reserver keywords for language
RESERVED_KEYWORDS = {
    'BEGIN': Token('BEGIN', 'BEGIN'),
    'END': Token('END', 'END'),

    'num'   : Token('NUM', 'NUM'),
    'str'   : Token('STR', 'STR'),
    'arr'   : Token('ARR', 'ARR'),

    'cond'  : Token('COND', 'COND'),
    'else'  : Token('ELSE', 'ELSE'),
    'do'    : Token('DO', 'DO'),
    'verchu': Token('VERCHU', 'VERCHU'),
    'print' : Token('PRINT', 'PRINT')
}
