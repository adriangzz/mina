import yacc
from calclex import tokens, lexer


def p_expression_program(p):
    '''
    program : PROGRAM_ID ID SEMICOLON block
    '''
    p[0] = p[1]


def p_expression_program_vars(p):
    '''
    program : PROGRAM_ID ID SEMICOLON vars block
    '''


def p_block(p):
    '''
    block : OPEN_BRACKET block_statue CLOSE_BRACKET
    '''
    p[0] = p[2]


def p_block_statue(p):
    '''
    block_statue : statue block_statue
                 | empty
    '''
    p[0] = p[1]


def p_statue(p):
    '''
    statue : assign
           | condition
           | write
    '''
    p[0] = p[1]


def p_vars(p):
    '''
    vars : VAR_ID varstype vars2
    vars2 : varstype vars2
          | empty
    varstype : ID varstype2 COLON type SEMICOLON
    varstype2 : COMMA ID varstype2
              | empty
    '''


def p_assign(p):
    '''
    assign : ID EQUAL expression SEMICOLON
    '''
    p[0] = ('=', p[1], p[3])


def p_exp(p):
    '''
    exp : term plus_minus
    '''


def p_term(p):
    '''
    term : factor multiply_divide
    '''


def p_factor(p):
    '''
    factor : OPEN_PARENTHESIS expression CLOSE_PARENTHESIS
           | plus_minus_factor var_cte
    '''


def p_var_cte(p):
    '''
    var_cte : ID 
            | INT 
            | FLOAT
    '''


def p_plus_minus_factor(p):
    '''
    plus_minus_factor : PLUS 
                      | MINUS 
                      | empty
    '''


def p_multiply_divide(p):
    '''
    multiply_divide : MULTIPLY term 
                    | DIVIDE term 
                    | empty
    '''


def p_plus_minus(p):
    '''
    plus_minus : PLUS exp 
               | MINUS exp 
               | empty
    '''


def p_condition(p):
    '''
    condition : IF OPEN_PARENTHESIS expression CLOSE_PARENTHESIS block else SEMICOLON
    '''


def p_condition_else(p):
    '''
    else : ELSE block 
         | empty
    '''


def p_expression(p):
    '''
    expression : exp expression_def
    expression_def : GREATER_THAN exp 
               | LESS_THAN exp 
               | NOT_EQUAL exp 
               | empty
    '''


def p_write(p):
    '''
    write : PRINT OPEN_PARENTHESIS write_exp CLOSE_PARENTHESIS SEMICOLON
    '''


def p_write_exp(p):
    '''
    write_exp : expression
              | expression COMMA write_exp
              | STRING
              | STRING COMMA write_exp
    '''


def p_type(p):
    '''
    type : INT_ID
         | FLOAT_ID
    '''
    p[0] = p[1]


def p_empty(p):
    'empty :'
    pass


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!", p)


# Build the parser
parser = yacc.yacc()

while True:
    try:
        s = input('>> ')
    except EOFError:
        break
    if not s:
        continue
    result = parser.parse(s, lexer)
    print(result)
