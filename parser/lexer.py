from lib import lex

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'print': 'PRINT',
    'program': 'PROGRAM_ID',
    'var': 'VAR_ID',
    'float': 'FLOAT_ID',
    'int': 'INT_ID',
    'function': 'FUNCTION_ID',
    'return': 'RETURN_ID',
}

tokens = [
    'INT',
    'FLOAT',
    'EQUAL',
    'PLUS',
    'MINUS',
    'MULTIPLY',
    'DIVIDE',
    'OPEN_BRACKET',
    'CLOSE_BRACKET',
    'OPEN_PARENTHESIS',
    'CLOSE_PARENTHESIS',
    'LESS_THAN',
    'LESS_THAN_EQUAL',
    'GREATER_THAN',
    'GREATER_THAN_EQUAL',
    'NOT_EQUAL',
    'SEMICOLON',
    'COLON',
    'COMMA',
    'STRING',
    'ID'
] + list(reserved.values())

t_SEMICOLON = r';'
t_COLON = r':'
t_COMMA = r','

t_OPEN_BRACKET = r'\{'
t_CLOSE_BRACKET = r'\}'
t_OPEN_PARENTHESIS = r'\('
t_CLOSE_PARENTHESIS = r'\)'

t_EQUAL = r'\='
t_LESS_THAN = r'\<'
t_LESS_THAN_EQUAL = r'\<='
t_GREATER_THAN = r'\>'
t_GREATER_THAN_EQUAL = r'\>='
t_NOT_EQUAL = r'\<>'

t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'\/'

t_STRING = r'"([^"]|\\")*"'


def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t


def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


t_ignore = ' \t'


def t_ID(t):
    r'_?[a-zA-Z][a-zA-Z0-9]*'
    t.type = reserved.get(t.value, 'ID')    # Check for reserved words
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()

data = """
program adrian;
var a, b, c, _d : int; j : float;
function int five(int a) {
    a = 6;
    return a;
}
{
    a = 5 + 4;
    b = a;
    c = 45;
    _d = 66;
    j = 4.5;
    if (a > c ) {
        a = 50;
    } else {
        c = 10;
    }
    print(c);
    a=b;
}

"""

# # Give the lexer some input
# lexer.input(data)

# # Tokenize
# while True:
#     tok = lexer.token()
#     if not tok:
#         break      # No more input
#     print(tok)