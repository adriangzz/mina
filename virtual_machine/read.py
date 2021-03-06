import json
import sys
import os
import statistics
import matplotlib.pyplot as plt
from re import I
from parser.variable_address import VariablesAddress

from parser.variable_semantics import FunctionTable
from virtual_machine.memory import Memory


class ReadObjFile(object):
    '''
    Class to read object file and create function and constant tables.
    '''

    def __init__(self, fileName='obj.json') -> None:
        self.table = FunctionTable()
        self.fileName = fileName
        self.quads = {}
        self.variableAddress = VariablesAddress()
        self.memory = Memory()
        self.instructionsStack = []
        self.currentFunctionCall = ""

    def readObjFile(self) -> None:
        '''
        Function to parse object file and generate
        function and constant variables and to store the quads.
        '''
        with open(self.fileName) as json_file:
            data = json.load(json_file)
            self.loadData(data)

        iP = 1
        instruction = ""
        while(iP <= len(self.quads)):
            instruction = self.quads[iP - 1][0]
            iPChanged = False

            if instruction == '1':
                data1 = self.quads[iP - 1][1]
                data2 = self.quads[iP - 1][2]

                if isinstance(data1, str):
                    if data1[0] == '*':
                        data1 = int(data1[1:])
                    else:
                        data1 = int(data1[1:])
                        data1 = self.memory.getMemoryValue(data1)
                        data1 = self.memory.getMemoryValue(data1)
                else:
                    data1 = self.memory.getMemoryValue(data1)

                if isinstance(data2, str):
                    if data2[0] == '*':
                        data2 = int(data2[1:])
                    else:
                        data2 = int(data2[1:])
                        data2 = self.memory.getMemoryValue(data2)
                        data2 = self.memory.getMemoryValue(data2)
                else:
                    data2 = self.memory.getMemoryValue(data2)

                aux = data1 + data2
                address = self.quads[iP - 1][3]
                self.memory.setMemoryValue(address, aux)
            elif instruction == '2':
                data1 = self.memory.getMemoryValue(
                    self.quads[iP - 1][1])
                data2 = self.memory.getMemoryValue(
                    self.quads[iP - 1][2])
                aux = data1 - data2
                address = self.quads[iP - 1][3]
                self.memory.setMemoryValue(address, aux)
            elif instruction == '3':
                data1 = self.memory.getMemoryValue(
                    self.quads[iP - 1][1])
                data2 = self.memory.getMemoryValue(
                    self.quads[iP - 1][2])
                aux = data1 * data2
                address = self.quads[iP - 1][3]
                self.memory.setMemoryValue(address, aux)
            elif instruction == '4':
                data1 = self.memory.getMemoryValue(
                    self.quads[iP - 1][1])
                data2 = self.memory.getMemoryValue(
                    self.quads[iP - 1][2])
                aux = data1 / data2
                address = self.quads[iP - 1][3]
                self.memory.setMemoryValue(address, aux)
            elif instruction == '5':
                data1 = self.quads[iP - 1][1]
                data2 = self.quads[iP - 1][2]

                if isinstance(data1, str):
                    data1 = int(data1[1:])
                    data1 = self.memory.getMemoryValue(data1)
                    data1 = self.memory.getMemoryValue(data1)
                else:
                    data1 = self.memory.getMemoryValue(data1)

                if isinstance(data2, str):
                    data2 = int(data2[1:])
                    data2 = self.memory.getMemoryValue(data2)
                    data2 = self.memory.getMemoryValue(data2)
                else:
                    data2 = self.memory.getMemoryValue(data2)

                aux = data1 < data2
                address = self.quads[iP - 1][3]
                self.memory.setMemoryValue(address, aux)
            elif instruction == '6':
                data1 = self.quads[iP - 1][1]
                data2 = self.quads[iP - 1][2]

                if isinstance(data1, str):
                    data1 = int(data1[1:])
                    data1 = self.memory.getMemoryValue(data1)
                    data1 = self.memory.getMemoryValue(data1)
                else:
                    data1 = self.memory.getMemoryValue(data1)

                if isinstance(data2, str):
                    data2 = int(data2[1:])
                    data2 = self.memory.getMemoryValue(data2)
                    data2 = self.memory.getMemoryValue(data2)
                else:
                    data2 = self.memory.getMemoryValue(data2)

                aux = data1 > data2
                address = self.quads[iP - 1][3]
                self.memory.setMemoryValue(address, aux)
            elif instruction == '7':
                data1 = self.quads[iP - 1][1]
                data2 = self.quads[iP - 1][2]

                if isinstance(data1, str):
                    data1 = int(data1[1:])
                    data1 = self.memory.getMemoryValue(data1)
                    data1 = self.memory.getMemoryValue(data1)
                else:
                    data1 = self.memory.getMemoryValue(data1)

                if isinstance(data2, str):
                    data2 = int(data2[1:])
                    data2 = self.memory.getMemoryValue(data2)
                    data2 = self.memory.getMemoryValue(data2)
                else:
                    data2 = self.memory.getMemoryValue(data2)

                aux = data1 <= data2
                address = self.quads[iP - 1][3]
                self.memory.setMemoryValue(address, aux)
            elif instruction == '8':
                data1 = self.quads[iP - 1][1]
                data2 = self.quads[iP - 1][2]

                if isinstance(data1, str):
                    data1 = int(data1[1:])
                    data1 = self.memory.getMemoryValue(data1)
                    data1 = self.memory.getMemoryValue(data1)
                else:
                    data1 = self.memory.getMemoryValue(data1)

                if isinstance(data2, str):
                    data2 = int(data2[1:])
                    data2 = self.memory.getMemoryValue(data2)
                    data2 = self.memory.getMemoryValue(data2)
                else:
                    data2 = self.memory.getMemoryValue(data2)

                aux = data1 >= data2
                address = self.quads[iP - 1][3]
                self.memory.setMemoryValue(address, aux)
            elif instruction == '9':
                data1 = self.quads[iP - 1][1]
                data2 = self.quads[iP - 1][2]

                if isinstance(data1, str):
                    data1 = int(data1[1:])
                    data1 = self.memory.getMemoryValue(data1)
                    data1 = self.memory.getMemoryValue(data1)
                else:
                    data1 = self.memory.getMemoryValue(data1)

                if isinstance(data2, str):
                    data2 = int(data2[1:])
                    data2 = self.memory.getMemoryValue(data2)
                    data2 = self.memory.getMemoryValue(data2)
                else:
                    data2 = self.memory.getMemoryValue(data2)

                aux = data1 == data2
                address = self.quads[iP - 1][3]
                self.memory.setMemoryValue(address, aux)
            elif instruction == '10':
                data1 = self.quads[iP - 1][1]
                data2 = self.quads[iP - 1][2]

                if isinstance(data1, str):
                    data1 = int(data1[1:])
                    data1 = self.memory.getMemoryValue(data1)
                    data1 = self.memory.getMemoryValue(data1)
                else:
                    data1 = self.memory.getMemoryValue(data1)

                if isinstance(data2, str):
                    data2 = int(data2[1:])
                    data2 = self.memory.getMemoryValue(data2)
                    data2 = self.memory.getMemoryValue(data2)
                else:
                    data2 = self.memory.getMemoryValue(data2)

                aux = data1 != data2
                address = self.quads[iP - 1][3]
                self.memory.setMemoryValue(address, aux)
            elif instruction == '11':
                iP = self.quads[iP - 1][3]
                iPChanged = True
            elif instruction == '12':
                data1 = self.memory.getMemoryValue(self.quads[iP - 1][2])
                if not data1:
                    iP = self.quads[iP - 1][3]
                    iPChanged = True
            elif instruction == '13':
                data1 = self.memory.getMemoryValue(self.quads[iP - 1][2])
                if data1:
                    iP = self.quads[iP - 1][3]
                    iPChanged = True
            elif instruction == '14':
                data1 = self.quads[iP - 1][3]
                if isinstance(data1, str):
                    data1 = int(data1[1:])
                    data1 = self.memory.getMemoryValue(data1)
                    data1 = self.memory.getMemoryValue(data1)
                else:
                    data1 = self.memory.getMemoryValue(data1)
                print(data1)
            elif instruction == '15':
                address = self.quads[iP - 1][3]
                if isinstance(address, str):
                    address = int(address[1:])
                    address = self.memory.getMemoryValue(address)
                    type = self.variableAddress.getType(address)[1]
                else:
                    type = self.variableAddress.getType(address)[1]
                aux = input()
                if type == 'int':
                    aux = int(aux)
                elif type == 'float':
                    aux = float(aux)
                elif type == 'bool':
                    aux = bool(aux)
                self.memory.setMemoryValue(address, aux)
            elif instruction == '16':
                self.memory.deleteLocalMemory()
                self.memory.deleteCurrentMemory()
                iP = self.instructionsStack.pop()
                iPChanged = True
            elif instruction == '17':
                functionName = self.quads[iP - 1][3]
                self.memory.addLocalMemory(
                    self.table.getFunction(functionName))
                self.currentFunctionCall = functionName
            elif instruction == '18':
                address = self.quads[iP - 1][2]
                pNum = self.quads[iP - 1][3] - 1
                paramType = self.table.getParameter(
                    self.currentFunctionCall, pNum)
                self.memory.addLocalParameters(address, pNum, paramType)
            elif instruction == '19':
                function = self.quads[iP - 1][3]

                iP += 1
                self.instructionsStack.append(iP)
                self.memory.setCurrentMemory()
                iP = self.table.getFunctionStartingAddress(function)
                iPChanged = True
            elif instruction == '20':
                data1 = self.quads[iP - 1][1]
                if isinstance(data1, str):
                    data1 = int(data1[1:])
                    data1 = self.memory.getMemoryValue(data1)
                    data1 = self.memory.getMemoryValue(data1)
                else:
                    data1 = self.memory.getMemoryValue(data1)

                address = self.quads[iP - 1][3]
                if isinstance(address, str):
                    address = int(address[1:])
                    address = self.memory.getMemoryValue(address)

                self.memory.setMemoryValue(address, data1)
            elif instruction == '21':
                data1 = self.quads[iP - 1][1]
                if isinstance(data1, str):
                    data1 = int(data1[1:])
                    data1 = self.memory.getMemoryValue(data1)
                    data1 = self.memory.getMemoryValue(data1)
                else:
                    data1 = self.memory.getMemoryValue(data1)
                limit = self.quads[iP - 1][3]
                if data1 < 0 or data1 >= limit:
                    sys.exit('Error: trying to access index out of bounds')

            elif instruction == '22':
                data1 = self.quads[iP - 1][1]
                if isinstance(data1, str):
                    if data1[0] == '*':
                        data1 = int(data1[1:])
                    else:
                        data1 = int(data1[1:])
                        data1 = self.memory.getMemoryValue(data1)
                        data1 = self.memory.getMemoryValue(data1)
                else:
                    data1 = self.memory.getMemoryValue(data1)

                data2 = self.quads[iP - 1][2]
                if isinstance(data2, str):
                    if data2[0] == '*':
                        data2 = int(data2[1:])
                    else:
                        data2 = int(data2[1:])
                        data2 = self.memory.getMemoryValue(data2)
                        data2 = self.memory.getMemoryValue(data2)
                else:
                    data2 = self.memory.getMemoryValue(data2)
                aux = data1 and data2
                address = self.quads[iP - 1][3]
                self.memory.setMemoryValue(address, aux)
            elif instruction == '23':
                data1 = self.quads[iP - 1][1]
                if isinstance(data1, str):
                    if data1[0] == '*':
                        data1 = int(data1[1:])
                    else:
                        data1 = int(data1[1:])
                        data1 = self.memory.getMemoryValue(data1)
                        data1 = self.memory.getMemoryValue(data1)
                else:
                    data1 = self.memory.getMemoryValue(data1)

                data2 = self.quads[iP - 1][2]
                if isinstance(data2, str):
                    if data2[0] == '*':
                        data2 = int(data2[1:])
                    else:
                        data2 = int(data2[1:])
                        data2 = self.memory.getMemoryValue(data2)
                        data2 = self.memory.getMemoryValue(data2)
                else:
                    data2 = self.memory.getMemoryValue(data2)
                aux = data1 or data2
                address = self.quads[iP - 1][3]
                self.memory.setMemoryValue(address, aux)
            elif instruction == '24':
                arr = []
                address = self.quads[iP - 1][1]
                addressTemp = self.quads[iP - 1][3]
                size = self.quads[iP - 1][2]

                for i in range(size):
                    arr.append(self.memory.getMemoryValue(address + i))
                aux = statistics.mean(arr)
                self.memory.setMemoryValue(addressTemp, aux)
            elif instruction == '25':
                arr = []
                address = self.quads[iP - 1][1]
                addressTemp = self.quads[iP - 1][3]
                size = self.quads[iP - 1][2]

                for i in range(size):
                    arr.append(self.memory.getMemoryValue(address + i))
                aux = statistics.median(arr)
                self.memory.setMemoryValue(addressTemp, aux)
            elif instruction == '26':
                arr = []
                address = self.quads[iP - 1][1]
                addressTemp = self.quads[iP - 1][3]
                size = self.quads[iP - 1][2]

                for i in range(size):
                    arr.append(self.memory.getMemoryValue(address + i))
                aux = statistics.mode(arr)
                self.memory.setMemoryValue(addressTemp, aux)
            elif instruction == '27':
                arr = []
                address = self.quads[iP - 1][1]
                addressTemp = self.quads[iP - 1][3]
                size = self.quads[iP - 1][2]

                for i in range(size):
                    arr.append(self.memory.getMemoryValue(address + i))
                aux = statistics.variance(arr)
                self.memory.setMemoryValue(addressTemp, aux)

            elif instruction == '28':
                arr1 = []
                arr2 = []
                address1 = self.quads[iP - 1][1]
                address2 = self.quads[iP - 1][2]
                size = self.quads[iP - 1][3]

                for i in range(size):
                    arr1.append(self.memory.getMemoryValue(address1 + i))
                    arr2.append(self.memory.getMemoryValue(address2 + i))

                plt.scatter(arr1, arr2)
                plt.show()
            else:
                pass

            if not iPChanged:
                iP += 1

    def loadData(self, data: map) -> None:
        '''
        Function to load data map into its tables.
        Creates the memory for global variables, constants and main function.
        '''
        self.table.setFunctionMap(data['functionTable'])
        self.table.setConstantTable(data['constantTable'])
        self.quads = data['quads']
        self.memory.loadConstantsInMemory(self.table.getConstants())
        self.memory.loadGlobalsInMemory(
            self.table.getFunction(data['programName']))
        self.memory.addLocalMemory(self.table.getFunction('main'))
        self.memory.setCurrentMemory()

    def deleteObjFile(self) -> None:
        '''
        Function to delete object file after use.
        '''
        os.remove(self.fileName)
