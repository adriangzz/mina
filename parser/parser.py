from lib import yacc
from parser.lexer import tokens, lexer
from parser.quadruples import Quadruples
from parser.variable_semantics import FunctionTable
import re

table = FunctionTable()
quad = Quadruples()


def p_expression_program(p):
    '''
    program : program_id SEMICOLON vars_functions main
    '''


def p_program_id(p):
    '''
    program_id : PROGRAM_ID ID
    '''
    table.setProgramName(p[2])
    table.addFunction({'name': p[2], 'type': 'void', 'variables': {}})


def p_vars_functions(p):
    '''
    vars_functions : vars functions vars_functions
                   | empty
    '''


def p_main(p):
    '''
    main : main_id block
    '''


def p_main_id(p):
    '''
    main_id : MAIN_ID OPEN_PARENTHESIS CLOSE_PARENTHESIS
    '''
    table.addFunction({'name': p[1], 'variables': {}})


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
    statue : vars
           | assign
           | condition
           | write
           | return
    '''


def p_vars(p):
    '''
    vars : VAR_ID type varstype
         | empty
    '''


def p_vars_type(p):
    '''
    varstype : assign_id_arr varstype2 SEMICOLON
    varstype2 : COMMA assign_id_arr varstype2
              | empty
    '''


def p_assign_id_arr(p):
    '''
    assign_id_arr : ID
                  | ARRAY
    '''
    # Get current type
    currType = table.getCurrentType()

    # Get var name without brackets
    varName = re.findall('_?[a-zA-Z][a-zA-Z0-9]*', p[1])[0]
    table.addVariables({'name': varName, 'type': currType})


def p_id_arr(p):
    '''
    id_arr : ID
           | ARRAY
    '''
    # Get var name without brackets
    varName = re.findall('_?[a-zA-Z][a-zA-Z0-9]*', p[1])[0]
    var = table.getVariable(varName)

    quad.push(var['name'], var['type'])
    quad.checkOperator(['*', '/'])


def p_functions(p):
    '''
    functions : functions_id OPEN_PARENTHESIS parameters CLOSE_PARENTHESIS block
              | empty
    '''
    if len(p) > 2:
        # Delete function table after finishing parsing
        table.deleteFunctionVariables(table.getCurrentFunction())
        table.setCurrentFunction(table.getProgramName())


def p_functions_id(p):
    '''
    functions_id : FUNCTION_ID type ID
    '''
    table.addFunction({'name': p[3], 'type': p[2], 'variables': {}})


def p_parameters(p):
    '''
    parameters : type assign_id_arr parameters2 
               | empty
    parameters2 : COMMA type assign_id_arr parameters2
                | empty 
    '''


def p_assign(p):
    '''
    assign : id_arr equal_assign expression SEMICOLON
    '''
    quad.checkOperatorLowLevel(['='])


def p_equal_assign(p):
    '''
    equal_assign : EQUAL_ASSIGN
    '''
    quad.push(p[1], "operator")


def p_exp(p):
    '''
    exp : term 
        | term plus_minus exp
    '''


def p_term(p):
    '''
    term : factor 
         | factor multiply_divide term
    '''
    quad.checkOperator(['+', '-'])


def p_factor(p):
    '''
    factor : open_parenthesis expression close_parenthesis
           | plus_minus var_cte
           | var_cte
    '''


def p_open_parenthesis(p):
    '''
    open_parenthesis : OPEN_PARENTHESIS
    '''
    quad.push(p[1], "operator")


def p_close_parenthesis(p):
    '''
    close_parenthesis : CLOSE_PARENTHESIS
    '''
    quad.push(p[1], "operator")


def p_var_cte(p):
    '''
    var_cte : int 
            | float
    '''
    quad.checkOperator(['*', '/'])


def p_int(p):
    '''
    int : INT
    '''
    quad.push(p[1], "int")


def p_float(p):
    '''
    float : FLOAT
    '''
    quad.push(p[1], "float")


def p_var_cte_ID(p):
    '''
    var_cte : ID
            | ARRAY 
    '''
    # Get var name without brackets
    varName = re.findall('_?[a-zA-Z][a-zA-Z0-9]*', p[1])[0]
    var = table.getVariable(varName)

    quad.push(var['name'], var['type'])
    quad.checkOperator(['*', '/'])


def p_multiply_divide(p):
    '''
    multiply_divide : MULTIPLY
                    | DIVIDE 

    '''
    quad.push(p[1], "operator")


def p_plus_minus(p):
    '''
    plus_minus : PLUS 
               | MINUS
    '''
    quad.push(p[1], "operator")


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
               | string 
               | exp comparison exp 
    '''
    quad.checkOperator(['>', '<', '>=', '<=', '==', '!='])


def p_string(p):
    '''
    string : STRING
    '''
    quad.push(p[1], 'string')


def p_comparison(p):
    '''
    comparison : GREATER_THAN
               | LESS_THAN
               | LESS_THAN_EQUAL
               | NOT_EQUAL
               | EQUAL
    '''
    quad.push(p[1], "operator")


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
    write_exp : write_expression
              | write_expression COMMA write_exp
    '''


def p_write_expression(p):
    '''
    write_expression : expression
    '''
    quad.createQuadPrint()


def p_type(p):
    '''
    type : INT_ID
         | FLOAT_ID
         | BOOL_ID
    '''
    table.setCurrentType(p[1])


def p_empty(p):
    '''
    empty :
    '''


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!", p)


def parseFile(file):
    # Build the parser
    parser = yacc.yacc()

    # Parse the file
    parser.parse(file, lexer)
    # print(table.getFunctions())
    quad.print()
    table.deleteTable()
