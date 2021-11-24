from lib import yacc
from parser.lexer import tokens, lexer
from parser.obj_file import ObjectFile
from parser.quadruples import Quadruples
from parser.variable_address import VariablesAddress
from parser.variable_semantics import FunctionTable
import sys

table = FunctionTable()
variableAddress = VariablesAddress()
quad = Quadruples(variableAddress, table)
obj_file = ObjectFile(quad, table)


def p_expression_program(p):
    '''
    program : program_id SEMICOLON vars_functions main
    '''


def p_program_id(p):
    '''
    program_id : PROGRAM_ID ID
    '''
    table.setProgramName(p[2])
    table.addFunction(
        {'name': p[2], 'returnType': 'void', 'type': 'program', 'variables': {}, 'size': {}}, 'global')
    quad.createQuadGoTo('GOTO', False)


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
    table.addFunction(
        {'name': p[1], 'returnType': 'void', 'type': 'main', 'variables': {}, 'size': {}}, 'local')
    quad.updateQuadGoTo()


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
           | while_condition
           | do_while_condition
           | for_condition
           | read
           | write
           | return
           | call SEMICOLON
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


def p_assign_id(p):
    '''
    assign_id_arr : ID
    '''
    # Get current type
    currType = table.getCurrentType()

    address = variableAddress.getTypeStartingAddress(
        table.getCurrentFunctionScope(), currType)
    table.addVariables({'name': p[1], 'type': currType, 'address': address})


def p_assign_id_arr_1d(p):
    '''
    assign_id_arr : ID OPEN_SQUARE_BRACKET INT CLOSE_SQUARE_BRACKET
    '''
    limit = p[3]

    # Get current type
    currType = table.getCurrentType()

    address = variableAddress.getTypeStartingAddress(
        table.getCurrentFunctionScope(), currType, limit)
    table.addVariables(
        {'name': p[1], 'type': currType, 'address': address, 'dim': {'limit': limit, 'k': 0}}, None, limit)


def p_assign_id_arr_2d(p):
    '''
    assign_id_arr : ID OPEN_SQUARE_BRACKET INT CLOSE_SQUARE_BRACKET OPEN_SQUARE_BRACKET INT CLOSE_SQUARE_BRACKET
    '''
    limit1 = p[3]
    limit2 = p[6]

    size = limit1 * limit2
    m1 = size / limit1

    # Get current type
    currType = table.getCurrentType()

    address = variableAddress.getTypeStartingAddress(
        table.getCurrentFunctionScope(), currType, size)
    table.addVariables(
        {'name': p[1], 'type': currType, 'address': address, 'dim': {'limit': limit1, 'm1': m1, 'next': {'limit': limit2, 'k': 0}}}, None, size)


def p_assign_id_arr_parameters(p):
    '''
    assign_id_arr_param : ID
    '''
    # Get current type
    currType = table.getCurrentType()

    address = variableAddress.getTypeStartingAddress(
        table.getCurrentFunctionScope(), currType)
    table.addVariables({'name': p[1], 'type': currType, 'address': address})
    table.addParameters(currType)


def p_id_arr(p):
    '''
    id_arr : ID
    '''
    var = table.getVariable(p[1])

    quad.push(var['address'], var['type'])
    quad.checkOperator(['*', '/'], False)


def p_id_arr_1d(p):
    '''
    id_arr : ID OPEN_SQUARE_BRACKET expression CLOSE_SQUARE_BRACKET
    '''
    var = table.getVariable(p[1])
    quad.createQuadVerifyLimit(var['dim']['limit'])
    quad.createQuadWithAddress(var['address'], var['type'])

    quad.checkOperator(['*', '/'], False)


def p_functions(p):
    '''
    functions : functions_id OPEN_PARENTHESIS parameters CLOSE_PARENTHESIS block
              | empty
    '''
    if len(p) > 2:
        # Delete function table after finishing parsing and reset local variable address
        table.deleteFunctionVariables(table.getCurrentFunction())
        variableAddress.resetScope(table.getCurrentFunctionScope())

        # Verify function has return type if not void
        table.verifyHasReturn()
        quad.createQuadEndFunc()
        table.setCurrentFunction(table.getProgramName(), 'global')


def p_functions_id(p):
    '''
    functions_id : FUNCTION_ID type ID
    '''
    returnType = p[2]
    if returnType != 'void':
        address = variableAddress.getTypeStartingAddress(
            'global', returnType)
        table.addVariables(
            {'name': p[3], 'type': returnType, 'address': address})

    initAddress = quad.getQuadCounter()
    table.addFunction(
        {'name': p[3], 'returnType': returnType, 'type': 'function', 'address': initAddress, 'hasReturn': False, 'variables': {}, 'parameters': [], 'size': {}}, 'local')
    p[0] = p[3]


def p_parameters(p):
    '''
    parameters : type assign_id_arr_param parameters2 
               | empty
    parameters2 : COMMA type assign_id_arr_param parameters2
                | empty 
    '''


def p_assign(p):
    '''
    assign : id_arr equal_assign expression SEMICOLON
    '''
    quad.checkOperator(['='], True)


def p_equal_assign(p):
    '''
    equal_assign : EQUAL_ASSIGN
    '''
    quad.push(p[1], "operator")


def p_call(p):
    '''
    call : id_call OPEN_PARENTHESIS parameters_expression CLOSE_PARENTHESIS

    '''
    quad.checkEndOfParameters()
    quad.createQuadGoSUB(p[1])
    returnType = table.getFunctionReturnType(p[1])
    if returnType != 'void':
        quad.setGlobalVarToTemp(p[1])
    quad.push(')', "operator")


def p_id_call(p):
    '''
    id_call : ID

    '''
    quad.push('(', "operator")
    table.functionExists(p[1])
    quad.setCurrentFunctionCall(p[1])
    quad.createQuadEra(p[1])
    p[0] = p[1]


def p_parameters_expression(p):
    '''
    parameters_expression : expression_param
                          | expression_param COMMA parameters_expression
                          | empty

    '''


def p_expression_param(p):
    '''
    expression_param : expression

    '''
    quad.createQuadParameter()


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
    quad.checkOperator(['+', '-'], False)


def p_factor(p):
    '''
    factor : open_parenthesis expression close_parenthesis
           | plus_minus var_cte
           | var_cte
           | call
           | special_functions
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
            | string
            | char
    '''
    quad.checkOperator(['*', '/'], False)


def p_int(p):
    '''
    int : INT
    '''
    if table.isConstant(p[1]):
        address = table.getConstant(p[1])
        quad.push(address, 'int')
    else:
        address = variableAddress.getTypeStartingAddress('constant', 'int')
        table.addConstant(p[1], address, 'int')
        quad.push(address, 'int')


def p_float(p):
    '''
    float : FLOAT
    '''
    if table.isConstant(p[1]):
        address = table.getConstant(p[1])
        quad.push(address, 'float')
    else:
        address = variableAddress.getTypeStartingAddress('constant', 'float')
        table.addConstant(p[1], address, 'float')
        quad.push(address, 'float')


def p_string(p):
    '''
    string : STRING
    '''
    string = p[1][1:-1]
    if table.isConstant(string):
        address = table.getConstant(string)
        quad.push(address, 'string')
    else:
        address = variableAddress.getTypeStartingAddress('constant', 'string')
        table.addConstant(string, address, 'string')
        quad.push(address, 'string')


def p_char(p):
    '''
    char : CHAR
    '''
    if table.isConstant(p[1]):
        address = table.getConstant(p[1])
        quad.push(address, 'char')
    else:
        address = variableAddress.getTypeStartingAddress('constant', 'char')
        table.addConstant(p[1], address, 'char')
        quad.push(address, 'char')


def p_var_cte_ID(p):
    '''
    var_cte : ID
    '''
    var = table.getVariable(p[1])

    quad.push(var['address'], var['type'])
    quad.checkOperator(['*', '/'], False)


def p_var_cte_arr(p):
    '''
    var_cte : id_arr_call OPEN_SQUARE_BRACKET expression CLOSE_SQUARE_BRACKET
    '''
    var = table.getVariable(p[1])
    quad.createQuadVerifyLimit(var['dim']['limit'])
    quad.createQuadWithAddress(var['address'], var['type'])

    quad.checkOperator(['*', '/'], False)
    quad.push(')', "operator")


def p_var_cte_arr_id(p):
    '''
    id_arr_call : ID
    '''
    quad.push('(', "operator")
    p[0] = p[1]


def p_special_functions(p):
    '''
    special_functions : MEAN OPEN_PARENTHESIS ID CLOSE_PARENTHESIS
                      | MEDIAN OPEN_PARENTHESIS ID CLOSE_PARENTHESIS
                      | MODE OPEN_PARENTHESIS ID CLOSE_PARENTHESIS
                      | VARIANCE OPEN_PARENTHESIS ID CLOSE_PARENTHESIS
    '''
    var = table.getVariable(p[3])
    if 'dim' not in var:
        sys.error("Error: Statistic functions must recieve an array as parameter")

    quad.createQuadSpecialFunc(
        p[1], var['address'], var['type'], var['dim']['limit'])


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
    condition : IF OPEN_PARENTHESIS expression close_parenthesis_condition block
    '''
    quad.updateQuadGoTo()


def p_condition_with_else(p):
    '''
    condition : IF OPEN_PARENTHESIS expression close_parenthesis_condition block_condition else
    '''


def p_while_condition(p):
    '''
    while_condition : while OPEN_PARENTHESIS expression close_parenthesis_condition block_condition_while
    '''


def p_while(p):
    '''
    while : WHILE
    '''
    quad.appendGoTo(1)


def p_do_while_condition(p):
    '''
    do_while_condition : do block WHILE OPEN_PARENTHESIS expression close_parenthesis_do
    '''


def p_do(p):
    '''
    do : DO
    '''
    quad.appendGoTo(0)


def p_close_parenthesis_condition(p):
    '''
    close_parenthesis_condition : CLOSE_PARENTHESIS
    '''
    quad.createQuadGoTo('GOTOF', False)


def p_close_parenthesis_do(p):
    '''
    close_parenthesis_do : CLOSE_PARENTHESIS
    '''
    quad.createQuadGoTo('GOTOT', True)


def p_for_condition(p):
    '''
    for_condition : FOR OPEN_PARENTHESIS id_for EQUAL_ASSIGN assign_exp_for TO exp_for_to CLOSE_PARENTHESIS block_condition_for
    '''


def p_for_condition_id(p):
    '''
    id_for : ID
    '''
    var = table.getVariable(p[1])
    if var['type'] == 'int':
        quad.push(var['address'], var['type'])
    else:
        sys.exit("Error: for variable must be of type int")


def p_assign_exp_for(p):
    '''
    assign_exp_for : expression
    '''
    quad.createQuadFor()


def p_exp_for_to(p):
    '''
    exp_for_to : expression
    '''
    quad.createQuadForTo()
    quad.createQuadGoTo('GOTOF', False)


def p_block_condition_for(p):
    '''
    block_condition_for : block
    '''
    quad.createQuadAddOneToFor()
    quad.updateQuadGoToWhile(0)


def p_block_condition(p):
    '''
    block_condition : block
    '''
    quad.updateQuadGoTo(1)
    quad.createQuadGoTo('GOTO', False)


def p_block_condition_while(p):
    '''
    block_condition_while : block
    '''
    quad.updateQuadGoToWhile(0)


def p_condition_else(p):
    '''
    else : ELSE block 
    '''
    quad.updateQuadGoTo()


def p_expression(p):
    '''
    expression : exp
               | string 
               | exp comparison exp 
               | expression logical expression 
    '''
    quad.checkOperator(['>', '<', '>=', '<=', '==', '!=', '&', '|'], False)


def p_string(p):
    '''
    string : STRING
    '''
    string = p[1][1:-1]
    if table.isConstant(string):
        address = table.getConstant(string)
        quad.push(address, 'string')
    else:
        address = variableAddress.getTypeStartingAddress('constant', 'string')
        table.addConstant(string, address, 'string')
        quad.push(address, 'string')


def p_comparison(p):
    '''
    comparison : GREATER_THAN
               | GREATER_THAN_EQUAL
               | LESS_THAN
               | LESS_THAN_EQUAL
               | NOT_EQUAL
               | EQUAL
    '''
    quad.push(p[1], "operator")


def p_logical(p):
    '''
    logical : AND
            | OR
    '''
    quad.push(p[1], "operator")


def p_return(p):
    '''
    return : RETURN_ID return_expression SEMICOLON
    '''


def p_return_expression(p):
    '''
    return_expression : expression
    '''
    lastOperandType = quad.getLastOperandType()
    table.verifyReturnType(lastOperandType)
    quad.createQuadReturn('=')
    quad.createQuadEndFunc()


def p_write(p):
    '''
    write : PRINT OPEN_PARENTHESIS write_exp CLOSE_PARENTHESIS SEMICOLON
    '''


def p_read(p):
    '''
    read : READ OPEN_PARENTHESIS read_exp CLOSE_PARENTHESIS SEMICOLON
    '''


def p_read_exp(p):
    '''
    read_exp : read_expression
             | read_expression COMMA read_exp
    '''


def p_read_expression(p):
    '''
    read_expression : id_arr
    '''
    quad.createQuadReadWriteReturn('read')


def p_write_exp(p):
    '''
    write_exp : write_expression
              | write_expression COMMA write_exp
    '''


def p_write_expression(p):
    '''
    write_expression : expression
    '''
    quad.createQuadReadWriteReturn('print')


def p_type(p):
    '''
    type : INT_ID
         | FLOAT_ID
         | BOOL_ID
         | CHAR_ID
         | VOID_ID
    '''
    table.setCurrentType(p[1])
    p[0] = p[1]


def p_empty(p):
    '''
    empty :
    '''


# Error rule for syntax errors
def p_error(p):
    sys.exit("Syntax error in input!", p)


def parseFile(file):
    # Build the parser
    parser = yacc.yacc()

    # Parse the file
    parser.parse(file, lexer)

    # Create object file
    obj_file.create()

    # Print object file
    # obj_file.print()

    # Delete table
    table.deleteTable()
