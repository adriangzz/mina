from collections import deque
from parser.variable_address import VariablesAddress
from parser.variable_semantics import FunctionTable, SemanticCube
import sys


class Quadruples(object):
    '''
    Class to create quadruples that will later be delivered to the virtual machine.
    '''

    def __init__(self, variableAddress: VariablesAddress, table: FunctionTable) -> None:
        self.stackOperands = []
        self.stackOperators = []
        self.stackQuads = []
        self.cube = SemanticCube()
        self.goTo = []
        self.quadCounter = 1
        self.variableAddress = variableAddress
        self.table = table
        self.currFunctionParameterCounter = 0
        self.currFunctionCall = ''
        self.operandCodes = {
            '+': '1',
            '-': '2',
            '*': '3',
            '/': '4',
            '<': '5',
            '>': '6',
            '<=': '7',
            '>=': '8',
            '==': '9',
            '!=': '10',
            'GOTO': '11',
            'GOTOF': '12',
            'GOTOT': '13',
            'print': '14',
            'read': '15',
            'ENDFunc': '16',
            'ERA': '17',
            'PARAM': '18',
            'GOSUB': '19',
            '=': '20',
            'VER': '21',
            '&': '22',
            '|': '23',
        }

    def push(self, o: str, type: str) -> None:
        '''
        Pushes operators or operands to their stack.
        '''
        if type == 'operator':
            self.stackOperators.append(o)
        else:
            self.stackOperands.append((o, type))

    def checkOperator(self, l: list, isLowLevel: bool) -> None:
        '''
        Check if operator exists in the given list, also checks if there is an end of bracket.
        If this conditions are met, createQuad method is called.
        '''
        if len(self.stackOperators) > 0:
            operator = self.stackOperators[-1]

            if operator in l:
                self.createQuad(operator, isLowLevel)
            elif operator == ')':
                self.stackOperators.pop()
                self.stackOperators.pop()
                self.checkOperator(['*', '/'], False)
                self.checkOperator(['+', '-'], False)

    def appendQuad(self, o: str, l: any, r: any, res: any) -> None:
        '''
        Appends a tuple of the given parameters to the quads list and adds 1 to the quad counter.
        '''
        o = self.getOperandCode(o)
        self.stackQuads.append(
            (o, l, r, res))
        self.quadCounter += 1

    def appendGoTo(self, counter: int) -> None:
        '''
        Appends a counter to the go to stack.
        '''
        self.goTo.append(self.quadCounter - counter)

    def createQuad(self, operator: str, isLowLevel: bool) -> None:
        '''
        Creates a quadruple given the operator.
        '''
        self.stackOperators.pop()
        rightOperandTuple = self.stackOperands.pop()
        leftOperandTuple = self.stackOperands.pop()

        rightOperand = rightOperandTuple[0]
        rightOperandType = rightOperandTuple[1]
        leftOperand = leftOperandTuple[0]
        leftOperandType = leftOperandTuple[1]

        resultType = self.cube.getResult(
            leftOperandType, rightOperandType, operator)

        if not isLowLevel:
            temp = self.variableAddress.getTypeStartingAddress(
                'local', 'temporal')
            self.stackOperands.append((temp, resultType))
            self.appendQuad(operator, leftOperand, rightOperand, temp)
            self.table.addSize('temporal')
        else:
            self.appendQuad(operator, rightOperand, None, leftOperand)

    def createQuadReadWriteReturn(self, type: str) -> None:
        '''
        Creates a quadruple for the print and read type.
        '''
        rightOperandTuple = self.stackOperands.pop()
        rightOperand = rightOperandTuple[0]

        self.appendQuad(type, None, None, rightOperand)

    def createQuadReturn(self, type: str) -> None:
        '''
        Creates a quadruple for the return type.
        '''
        rightOperandTuple = self.stackOperands.pop()
        rightOperand = rightOperandTuple[0]

        functionName = self.table.getCurrentFunction()
        globalVar = self.table.getVariable(functionName)

        self.appendQuad(type, rightOperand, None, globalVar['address'])

    def createQuadVerifyLimit(self, limit: int) -> None:
        '''
        Creates a quadruple to verify the index is within limits of the array.
        '''
        rightOperandTuple = self.stackOperands[-1]
        rightOperand = rightOperandTuple[0]

        self.appendQuad('VER', rightOperand, 0, limit)

    def createQuadWithAddress(self, address: int, type: str) -> None:
        '''
        Creates a quadruple to add the variable address.
        '''
        rightOperandTuple = self.stackOperands.pop()
        rightOperand = rightOperandTuple[0]

        temp = self.variableAddress.getTypeStartingAddress(
            'local', 'temporal')
        self.stackOperands.append(('(' + str(temp), 'int'))
        self.appendQuad('+', rightOperand, '*' + str(address), temp)
        self.table.addSize('temporal')

    def setGlobalVarToTemp(self, name: str) -> None:
        '''
        '''
        globalVar = self.table.getGlobalVariable(name)

        resultType = self.cube.getResult(
            globalVar['type'], globalVar['type'], '=')

        temp = self.variableAddress.getTypeStartingAddress(
            'local', 'temporal')
        self.stackOperands.append((temp, resultType))
        self.appendQuad('=', globalVar['address'], None, temp)
        self.table.addSize('temporal')

    def createQuadEndFunc(self) -> None:
        '''
        Creates a quadruple for the end function.
        '''
        self.appendQuad('ENDFunc', None, None, None)

    def createQuadEra(self, size: int) -> None:
        '''
        Creates a quadruple for the new size block call.
        '''
        self.appendQuad('ERA', None, None, size)
        self.currFunctionParameterCounter = 0

    def createQuadGoSUB(self, function: str) -> None:
        '''
        Creates a quadruple for gosub to the function call.
        '''
        address = self.table.getFunctionStartingAddress(function)
        self.appendQuad('GOSUB', None, None, function)

    def createQuadParameter(self) -> None:
        '''
        Creates a quadruple for the parameter.
        '''
        rightOperandTuple = self.stackOperands.pop()

        rightOperand = rightOperandTuple[0]
        rightOperandType = rightOperandTuple[1]

        parameterType = self.table.getParameter(self.currFunctionCall,
                                                self.currFunctionParameterCounter)

        if rightOperandType == parameterType:
            pNum = self.currFunctionParameterCounter + 1
            self.appendQuad('PARAM', None, rightOperand, pNum)
            self.currFunctionParameterCounter += 1
        else:
            sys.exit(
                f'Error: parameter of type {rightOperandType} is different from parameter of type {parameterType} expected')

    def checkEndOfParameters(self):
        '''
        Check function has gotten to the end of parameters
        '''
        paramCount = self.table.getParameterCount(self.currFunctionCall)
        if self.currFunctionParameterCounter != paramCount:
            sys.exit(
                f'Error: function {self.currFunctionCall} expected {paramCount} parameters and was only given {self.currFunctionParameterCounter}')

    def createQuadGoTo(self, type: str, appendCounter: bool = False) -> None:
        '''
        Creates a quadruple for the goto type.
        '''
        if type != 'GOTO':
            rightOperandTuple = self.stackOperands.pop()

            rightOperand = rightOperandTuple[0]
            rightOperandType = rightOperandTuple[1]

            if rightOperandType != 'bool' and rightOperandType != 'int' and rightOperandType != 'float':
                sys.exit("ERROR: condition must be of type bool, int or float")

            if appendCounter:
                prevGoTo = self.goTo.pop()
                self.appendQuad(type, None, rightOperand, prevGoTo)
            else:
                self.appendQuad(type, None, rightOperand, None)
                self.appendGoTo(2)
        else:
            self.appendQuad(type, None, None, None)
            self.appendGoTo(2)

    def updateQuadGoTo(self, extra: int = 0) -> None:
        '''
        Gets the last go to in the stack and updates the counter in it with the global quad counter.
        '''
        prevGoTo = self.goTo.pop()

        # Update goto with counter
        tupleList = list(self.stackQuads[prevGoTo])
        tupleList[3] = self.quadCounter + extra
        updatedTuple = tuple(tupleList)
        self.stackQuads[prevGoTo] = updatedTuple

    def updateQuadGoToWhile(self, extra: int = 0) -> None:
        '''
        Gets the last two go to's in the stack and updates the gotof and adds a new goto.
        '''
        prevGoToFalse = self.goTo.pop()
        prevGoToReturn = self.goTo.pop()

        self.appendQuad('GOTO', None, None, prevGoToReturn + 1)

        # Update goto with counter
        tupleList = list(self.stackQuads[prevGoToFalse])
        tupleList[3] = self.quadCounter + extra
        updatedTuple = tuple(tupleList)
        self.stackQuads[prevGoToFalse] = updatedTuple

    def getQuadCounter(self) -> int:
        '''
        Returns the current quad counter.
        '''
        return self.quadCounter

    def getLastOperandType(self) -> int:
        '''
        Returns the last operand type.
        '''
        operandTuple = self.stackOperands[-1]
        rightOperandType = operandTuple[1]
        return rightOperandType

    def setCurrentFunctionCall(self, name: str) -> None:
        '''
        Set the current function being called.
        '''
        self.currFunctionCall = name

    def getOperandCode(self, operand: str) -> str:
        '''
        Get the code given the operand.
        '''
        return self.operandCodes[operand]

    def getQuads(self) -> list:
        '''
        Get the quads.
        '''
        return self.stackQuads

    def print(self) -> None:
        '''
        Prints all the lists
        '''
        print(self.stackOperands)
        print(self.stackOperators)
        print(self.stackQuads)

    def printQuad(self) -> None:
        '''
        Prints the quadruples nicely
        '''
        for i, q in enumerate(self.stackQuads):
            print(f'{i + 1}. {q}')
