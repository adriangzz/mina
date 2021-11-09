from collections import deque
from parser.variable_address import VariablesAddress
from parser.variable_semantics import FunctionTable, SemanticCube


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
                self.checkOperator(['*', '/'])
                self.checkOperator(['+', '-'])

    def appendQuad(self, o: str, l: any, r: any, res: any) -> None:
        '''
        Appends a tuple of the given parameters to the quads list and adds 1 to the quad counter.
        '''
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
                'temporal', resultType)
            self.stackOperands.append((temp, resultType))
            self.appendQuad(operator, leftOperand, rightOperand, temp)
            self.table.addSize()
        else:
            self.appendQuad(operator, rightOperand, None, leftOperand)

    def createQuadReadWriteReturn(self, type: str) -> None:
        '''
        Creates a quadruple for the print and read type.
        '''
        rightOperandTuple = self.stackOperands.pop()

        rightOperand = rightOperandTuple[0]

        self.appendQuad(type, None, None, rightOperand)

    def createQuadEndFunc(self) -> None:
        '''
        Creates a quadruple for the end function.
        '''
        self.appendQuad('ENDFunc', None, None, None)

    def createQuadGoTo(self, type: str, appendCounter: bool = False) -> None:
        '''
        Creates a quadruple for the goto type.
        '''
        if type != 'GOTO':
            rightOperandTuple = self.stackOperands.pop()

            rightOperand = rightOperandTuple[0]
            rightOperandType = rightOperandTuple[1]

            if rightOperandType != 'bool' and rightOperandType != 'int' and rightOperandType != 'float':
                print("ERROR: condition must be of type bool, int or float")
                raise SyntaxError

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
        Returns the current quad counter
        '''
        return self.quadCounter

    def getLastOperandType(self) -> int:
        '''
        Returns the last operand type
        '''
        operandTuple = self.stackOperands[-1]
        rightOperandType = operandTuple[1]
        return rightOperandType

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
