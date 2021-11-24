from parser.variable_address import VariablesAddress


class Memory(object):
    '''
    Class to keep virtual memory, uses a dictionary of lists to keep track of memory for each type.
    It generates a list size given the memory needed.
    '''

    def __init__(self) -> None:
        self.globalMemory = {"int": [],
                             "float": [],
                             "char": [],
                             "bool": []}
        self.constantsMemory = {"int": [],
                                "float": [],
                                "char": [],
                                "bool": [],
                                "string": []}
        self.localMemoryStack = []
        self.currentMemoryStack = []
        self.variableAddress = VariablesAddress()

    def getMemoryValue(self, address: int) -> any:
        '''
        Gets the value in a memory address.
        '''
        addressInfo = self.variableAddress.getType(address)
        if addressInfo[0] == 'global':
            return self.globalMemory[addressInfo[1]][address - addressInfo[2]]
        elif addressInfo[0] == 'constant':
            return self.constantsMemory[addressInfo[1]][address - addressInfo[2]]
        else:
            return self.localMemoryStack[self.currentMemoryStack[-1]][addressInfo[1]][address - addressInfo[2]]

    def setMemoryValue(self, address: int, value: any) -> None:
        '''
        Sets the value in a memory address.
        '''
        addressInfo = self.variableAddress.getType(address)
        if addressInfo[0] == 'global':
            self.globalMemory[addressInfo[1]][address - addressInfo[2]] = value
        elif addressInfo[0] == 'constant':
            self.constantsMemory[addressInfo[1]
                                 ][address - addressInfo[2]] = value
        else:
            self.localMemoryStack[self.currentMemoryStack[-1]][addressInfo[1]
                                                               ][address - addressInfo[2]] = value

    def loadConstantsInMemory(self, constants: dict) -> None:
        '''
        Loads the constants in memory.
        '''
        # Create memory size
        for item in constants['size']:
            self.constantsMemory[item] = [None] * constants['size'][item]

        for item in constants['vars'].items():
            type = item[1][1]
            value = item[0]
            address = item[1][0]
            beginingAddress = self.variableAddress.getType(address)[2]

            if type == 'int':
                value = int(value)
            elif type == 'float':
                value = float(value)
            elif type == 'bool':
                value = bool(value)

            self.constantsMemory[type][address - beginingAddress] = value

    def loadGlobalsInMemory(self, globals: dict) -> None:
        '''
        Loads the global variables in memory.
        '''
        # Create memory size
        for item in globals['size']:
            self.globalMemory[item] = [None] * globals['size'][item]

    def addLocalMemory(self, locals: dict) -> None:
        '''
        Creates a local memory given the size.
        '''
        memory = {"int": [],
                  "float": [],
                  "char": [],
                  "bool": []}

        for item in locals['size']:
            memory[item] = [None] * locals['size'][item]

        self.localMemoryStack.append(memory)

    def addLocalParameters(self, address: int, param: int, paramType: str) -> None:
        '''
        Adds value to a parameter.
        '''
        value = self.getMemoryValue(address)
        self.localMemoryStack[-1][paramType][param] = value

    def deleteLocalMemory(self) -> None:
        '''
        Deletes the last local memory in the stack.
        '''
        self.localMemoryStack.pop()

    def setCurrentMemory(self) -> None:
        '''
        Sets the current memory in the stack.
        '''
        self.currentMemoryStack.append(len(self.localMemoryStack) - 1)

    def deleteCurrentMemory(self) -> None:
        '''
        Deletes the current memory in the stack.
        '''
        self.currentMemoryStack.pop()

    def printMemory(self) -> None:
        '''
        Prints the memory.
        '''
        print(self.globalMemory, self.constantsMemory, self.localMemoryStack)
