from collections import deque
from parser.variable_semantics import SemanticCube


class Quadruples(object):

    def __init__(self) -> None:
        self.stackOperands = []
        self.stackOperators = []
        self.stackQuads = []
        self.cube = SemanticCube()
        self.count = 1

    def push(self, o: str, type: str) -> None:
        if type == 'operator':
            self.stackOperators.append(o)
        else:
            self.stackOperands.append((o, type))

    def checkOperator(self, l: list) -> None:
        if len(self.stackOperators) > 0:
            operator = self.stackOperators[-1]

            if operator in l:
                self.createQuad(operator)
            elif operator == ')':
                self.stackOperators.pop()
                self.stackOperators.pop()
                self.checkOperator(['*', '/'])
                self.checkOperator(['+', '-'])

    def checkOperatorLowLevel(self, l: list):
        if len(self.stackOperators) > 0:
            operator = self.stackOperators[-1]

            if operator == 'print':
                self.createQuadPrint(operator)
            elif operator in l:
                self.createQuadLowLevel(operator)

    def createQuad(self, operator: str) -> None:
        self.stackOperators.pop()
        rightOperandTuple = self.stackOperands.pop()
        leftOperandTuple = self.stackOperands.pop()

        rightOperand = rightOperandTuple[0]
        rightOperandType = rightOperandTuple[1]
        leftOperand = leftOperandTuple[0]
        leftOperandType = leftOperandTuple[1]

        resultType = self.cube.getResult(
            leftOperandType, rightOperandType, operator)

        temp = 't' + str(self.count)

        self.stackQuads.append(
            (operator, leftOperand, rightOperand, temp))
        self.stackOperands.append((temp, resultType))

        self.count += 1

    def createQuadLowLevel(self, operator: str) -> None:
        self.stackOperators.pop()
        rightOperandTuple = self.stackOperands.pop()
        leftOperandTuple = self.stackOperands.pop()

        rightOperand = rightOperandTuple[0]
        rightOperandType = rightOperandTuple[1]
        leftOperand = leftOperandTuple[0]
        leftOperandType = leftOperandTuple[1]

        self.cube.getResult(
            leftOperandType, rightOperandType, operator)

        self.stackQuads.append(
            (operator, rightOperand, None, leftOperand))

    def createQuadPrint(self) -> None:
        rightOperandTuple = self.stackOperands.pop()

        rightOperand = rightOperandTuple[0]

        self.stackQuads.append(
            ('print', None, None, rightOperand))

    def print(self) -> None:
        print(self.stackOperands)
        print(self.stackOperators)
        print(self.stackQuads)
