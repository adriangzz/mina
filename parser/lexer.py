import sys
from lib import lex

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'to': 'TO',
    'do': 'DO',
    'print': 'PRINT',
    'read': 'READ',
    'program': 'PROGRAM_ID',
    'var': 'VAR_ID',
    'float': 'FLOAT_ID',
    'int': 'INT_ID',
    'bool': 'BOOL_ID',
    'char': 'CHAR_ID',
    'void': 'VOID_ID',
    'function': 'FUNCTION_ID',
    'return': 'RETURN_ID',
    'main': 'MAIN_ID',
    'mean': 'MEAN',
    'median': 'MEDIAN',
    'mode': 'MODE',
    'variance': 'VARIANCE',
}

tokens = [
    'INT',
    'FLOAT',
    'EQUAL_ASSIGN',
    'PLUS',
    'MINUS',
    'MULTIPLY',
    'DIVIDE',
    'OPEN_BRACKET',
    'CLOSE_BRACKET',
    'OPEN_PARENTHESIS',
    'OPEN_SQUARE_BRACKET',
    'CLOSE_PARENTHESIS',
    'CLOSE_SQUARE_BRACKET',
    'LESS_THAN',
    'LESS_THAN_EQUAL',
    'GREATER_THAN',
    'GREATER_THAN_EQUAL',
    'NOT_EQUAL',
    'EQUAL',
    'AND',
    'OR',
    'SEMICOLON',
    'COLON',
    'COMMA',
    'STRING',
    'CHAR',
    'ID',
] + list(reserved.values())

t_SEMICOLON = r';'
t_COLON = r':'
t_COMMA = r','

t_OPEN_BRACKET = r'\{'
t_CLOSE_BRACKET = r'\}'
t_OPEN_PARENTHESIS = r'\('
t_CLOSE_PARENTHESIS = r'\)'
t_OPEN_SQUARE_BRACKET = r'\['
t_CLOSE_SQUARE_BRACKET = r'\]'

t_EQUAL = r'\=='
t_EQUAL_ASSIGN = r'\='
t_LESS_THAN = r'\<'
t_LESS_THAN_EQUAL = r'\<='
t_GREATER_THAN = r'\>'
t_GREATER_THAN_EQUAL = r'\>='
t_NOT_EQUAL = r'\<>'
t_AND = r'\&'
t_OR = r'\|'

t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'\/'

t_STRING = r'"([^"]|\\")*"'
t_CHAR = r'\'.\''


def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t


def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


t_ignore = ' \t'

t_ignore_COMMENT = r'//.*'


def t_ID(t):
    r'_?[a-zA-Z][a-zA-Z0-9]*'
    t.type = reserved.get(t.value, 'ID')    # Check for reserved words
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    t.lexer.skip(1)
    sys.exit("Illegal character '%s'" % t.value[0])


lexer = lex.lex()
