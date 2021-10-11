from lib import yacc
from parser.lexer import tokens, lexer


def p_expression_program(p):
    '''
    program : PROGRAM_ID ID SEMICOLON block
    '''


def p_expression_program_vars(p):
    '''
    program : PROGRAM_ID ID SEMICOLON vars functions block
    '''


def p_block(p):
    '''
    block : OPEN_BRACKET block_statue CLOSE_BRACKET
    '''


def p_block_statue(p):
    '''
    block_statue : statue block_statue
                 | empty
    '''


def p_statue(p):
    '''
    statue : assign
           | condition
           | write
           | return
    '''


def p_vars(p):
    '''
    vars : VAR_ID varstype vars2
    vars2 : varstype vars2
          | empty
    varstype : id_arr varstype2 COLON type SEMICOLON
    varstype2 : COMMA id_arr varstype2
              | empty
    '''


def p_id_arr(p):
    '''
    id_arr : ID
           | ARRAY
    '''


def p_functions(p):
    '''
    functions : FUNCTION_ID type ID OPEN_PARENTHESIS parameters CLOSE_PARENTHESIS block
              | empty
    '''


def p_parameters(p):
    '''
    parameters : type ID parameters2 
               | empty
    parameters2 : COMMA type ID parameters2
                | empty 
    '''


def p_assign(p):
    '''
    assign : ID EQUAL expression SEMICOLON
    '''


def p_exp(p):
    '''
    exp : term 
        | term plus_minus exp
    '''
    if (len(p) == 2):
        p[0] = p[1]
    else:
        p[0] = (p[2], p[1], p[3])


def p_term(p):
    '''
    term : factor 
         | factor multiply_divide term
    '''
    if (len(p) == 2):
        p[0] = p[1]
    else:
        p[0] = (p[2], p[1], p[3])


def p_factor(p):
    '''
    factor : OPEN_PARENTHESIS expression CLOSE_PARENTHESIS
           | plus_minus_factor var_cte
           | var_cte
    '''
    if (len(p) == 4):
        p[0] = p[2]
    elif (len(p) == 3):
        p[0] = (p[1], p[2])
    else:
        p[0] = p[1]


def p_var_cte(p):
    '''
    var_cte : ID 
            | INT 
            | FLOAT
    '''
    p[0] = p[1]


def p_plus_minus_factor(p):
    '''
    plus_minus_factor : PLUS 
                      | MINUS 
                      | empty
    '''
    p[0] = p[1]


def p_multiply_divide(p):
    '''
    multiply_divide : MULTIPLY
                    | DIVIDE 

    '''
    p[0] = p[1]


def p_plus_minus(p):
    '''
    plus_minus : PLUS 
               | MINUS
    '''
    p[0] = p[1]


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
    expression : exp 
               | exp GREATER_THAN exp 
               | exp GREATER_THAN_EQUAL exp 
               | exp LESS_THAN exp 
               | exp LESS_THAN_EQUAL exp 
               | exp NOT_EQUAL exp 
    '''
    if (len(p) == 2):
        p[0] = run(p[1])
    else:
        p[0] = (p[2], p[1], p[3])


def p_return(p):
    '''
    return : RETURN_ID expression SEMICOLON
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
    print(p[1])


def p_type(p):
    '''
    type : INT_ID
         | FLOAT_ID
    '''


def p_empty(p):
    '''
    empty :
    '''
    p[0] = None


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!", p)


def run(p):
    if type(p) == tuple:
        if (p[0] == '+'):
            return run(p[1]) + run(p[2])
        if (p[0] == '-'):
            return run(p[1]) - run(p[2])
        if (p[0] == '*'):
            return run(p[1]) * run(p[2])
        if (p[0] == '/'):
            return run(p[1]) / run(p[2])
    else:
        return p


def parseFile(file):
    # Build the parser
    parser = yacc.yacc()

    # while True:
    # try:
    #     s = input('>> ')
    # except EOFError:
    #     break
    # if not s:
    #     continue
    result = parser.parse(file, lexer)
    print(result)
