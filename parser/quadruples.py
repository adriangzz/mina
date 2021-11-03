from collections import deque
from parser.variable_semantics import SemanticCube


class Quadruples(object):

    def __init__(self) -> None:
        self.stackOperands = []
        self.stackOperators = []
        self.stackQuads = []
        self.cube = SemanticCube()
        self.count = 1
        self.goTo = []

    def push(self, o: str, type: str) -> None:
        if type == 'operator':
            self.stackOperators.append(o)
        else:
            self.stackOperands.append((o, type))

    def checkOperator(self, l: list) -> None:
        if len(self.stackOperators) > 0:
            operator = self.stackOperators[-1]

            if operator in l:
                self.createQuad(operator, False)
            elif operator == ')':
                self.stackOperators.pop()
                self.stackOperators.pop()
                self.checkOperator(['*', '/'])
                self.checkOperator(['+', '-'])

    def checkOperatorLowLevel(self, l: list):
        if len(self.stackOperators) > 0:
            operator = self.stackOperators[-1]

            if operator in l:
                self.createQuad(operator, True)

    def createQuad(self, operator: str, isLowLevel: bool) -> None:
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
            temp = 't' + str(self.count)
            self.stackOperands.append((temp, resultType))
            self.stackQuads.append(
                (operator, leftOperand, rightOperand, temp))
            self.count += 1
        else:
            self.stackQuads.append(
                (operator, rightOperand, None, leftOperand))

    def createQuadReadWrite(self, type: str) -> None:
        rightOperandTuple = self.stackOperands.pop()

        rightOperand = rightOperandTuple[0]

        self.stackQuads.append(
            (type, None, None, rightOperand))

    def createQuadGoTo(self, type: str) -> None:
        rightOperandTuple = self.stackOperands.pop()

        rightOperand = rightOperandTuple[0]

        self.stackQuads.append(
            (type, None, rightOperand, None))

        self.goTo.append(len(self.stackQuads) - 1)

    def updateQuadGoTo(self) -> None:
        prevGoTo = self.goTo.pop()

        tupleList = list(self.stackQuads[prevGoTo])
        tupleList[3] = len(self.stackQuads) + 1
        updatedTuple = tuple(tupleList)

        self.stackQuads[prevGoTo] = updatedTuple

    def print(self) -> None:
        print(self.stackOperands)
        print(self.stackOperators)
        print(self.stackQuads)
