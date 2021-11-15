from parser.variable_address import VariablesAddress


class FunctionTable(object):
    '''
    Class to keep variable semantics.
    Created using a dictionary of dictionaries that stores the names of the functions as keys for O(N) search time
    and the rest of the values as a dictionary. e.j. {'funcName':{'name':'funcName','type':'int',...}}.
    Stores the latest added function name to add all the next variables to that scope.
    Variables are added to a new table added as a value to the function dictionary.
    '''

    def __init__(self) -> None:
        self.functionNameMap = {}
        self.constantTable = {}
        self.currFunction = ''
        self.currFunctionScope = ''
        self.programName = ''
        self.currType = ''

    def addFunction(self, row: dict, type: str) -> None:
        '''
        Checks name of function does not exist, then adds it to the dictionary using it's name as key.
        Sets current function as this function.
        Raises syntaxerror if function already exists.
        '''
        if row['name'] not in self.functionNameMap:
            self.functionNameMap[row['name']] = row
            self.currFunction = row['name']
            self.currFunctionScope = type
        else:
            print("Error: function name already in use")
            raise SyntaxError

    def addVariables(self, row: dict, name: str = None) -> None:
        '''
        Function to add variables to current function.
        Uses last added function as default, but an extra optional parameter with the name of the function is accepted.
        Adds 1 to the function size in the table.
        '''
        if name and name in self.functionNameMap and row['name'] not in self.functionNameMap[name]['variables']:
            self.functionNameMap[name]['variables'][row['name']] = row
        elif row['name'] not in self.functionNameMap[self.currFunction]['variables']:
            self.functionNameMap[self.currFunction]['variables'][row['name']] = row
        else:
            print("Error: variable name '" +
                  row['name'] + "' already in use")
            raise SyntaxError

        self.addSize()

    def addParameters(self, type: str) -> None:
        '''
        Function to add parameters types to current function table.
        '''
        self.functionNameMap[self.currFunction]['parameters'].append(type)

    def getParameter(self, function: str, idx: int) -> str:
        '''
        Function to get parameter type of given function and the index.
        '''
        paramCount = len(self.functionNameMap[function]['parameters'])
        if paramCount > idx:
            return self.functionNameMap[function]['parameters'][idx]
        else:
            print(
                f'Error: function {function} only takes {paramCount} arguments')
            raise SyntaxError

    def getParameterCount(self, function: str) -> str:
        '''
        Function to get parameter count of given function.
        '''
        return len(self.functionNameMap[function]['parameters'])

    def getFunction(self, name: str) -> dict:
        '''
        Function that returns the dictionary of the name of function given.
        Returns empty dict if name does not exist.
        '''
        if name in self.functionNameMap:
            return self.functionNameMap[name]
        return {}

    def addSize(self) -> None:
        '''
        Adds 1 to current function size.
        '''
        if self.functionNameMap[self.currFunction]['type'] == 'function':
            size = self.functionNameMap[self.currFunction]['size']
            self.functionNameMap[self.currFunction]['size'] = size + 1

    def getFunctions(self) -> dict:
        '''
        Returns the whole dictionary of functions and variables.
        '''
        return self.functionNameMap

    def deleteFunction(self, name: str) -> bool:
        '''
        Deletes function given the name.
        Returns true if deleted, false otherwise.
        '''
        if name in self.functionNameMap:
            self.functionNameMap.pop(name)
            return True
        return False

    def deleteFunctionVariables(self, name: str) -> None:
        '''
        Deletes function given the name.
        Returns true if deleted, false otherwise.
        '''
        if name in self.functionNameMap:
            self.functionNameMap[name].pop('variables')
        else:
            print(f'Error: function {name} not declared')
            raise SyntaxError

    def functionExists(self, name: str) -> None:
        '''
        Raises syntax error if funciton does not exist.
        '''
        if name not in self.functionNameMap:
            print(f'Error: function {name} not declared')
            raise SyntaxError

    def setCurrentFunction(self, name: str, scope: str) -> None:
        '''
        Sets current function.
        '''
        self.currFunction = name
        self.currFunctionScope = scope

    def getCurrentFunction(self) -> str:
        '''
        Gets current function.
        '''
        return self.currFunction

    def getCurrentFunctionScope(self) -> str:
        '''
        Gets current function.
        '''
        return self.currFunctionScope

    def getCurrentType(self) -> str:
        '''
        Returns current type.
        '''
        return self.currType

    def setCurrentType(self, name: str) -> None:
        '''
        Sets current type.
        '''
        self.currType = name

    def setProgramName(self, name: str) -> None:
        '''
        Sets program name.
        '''
        self.programName = name

    def getProgramName(self) -> str:
        '''
        Gets program name.
        '''
        return self.programName

    def getFuncitonSize(self, name: str) -> int:
        '''
        Gets function size.
        '''
        return self.functionNameMap[name]['size']

    def getVariable(self, name: str) -> dict:
        '''
        Checks if variable is declared and returns it's info, raises syntax error if not declared.
        '''
        if name in self.functionNameMap[self.currFunction]['variables']:
            return self.functionNameMap[self.currFunction]['variables'][name]
        elif name in self.functionNameMap[self.programName]['variables']:
            return self.functionNameMap[self.programName]['variables'][name]
        print(
            f'Error: variable {name} not declared in scope or global variables')
        raise SyntaxError

    def getGlobalVariable(self, name: str) -> dict:
        '''
        Returns the given function global variable.
        '''
        if name in self.functionNameMap[self.programName]['variables']:
            return self.functionNameMap[self.programName]['variables'][name]
        print(
            f'Error: variable {name} not declared in scope or global variables')
        raise SyntaxError

    def getFunctionReturnType(self, name: str) -> dict:
        '''
        Returns given function return type.
        '''
        return self.functionNameMap[name]['returnType']

    def deleteTable(self) -> None:
        '''
        Deletes table.
        '''
        del self.functionNameMap

    def isConstant(self, cons: any) -> bool:
        '''
        Check if constant exists in the table.
        '''
        return cons in self.constantTable

    def addConstant(self, cons: any, address: int) -> None:
        '''
        Adds constant to table.
        '''
        self.constantTable[cons] = address

    def getConstant(self, cons: any) -> int:
        '''
        Returns constant address.
        '''
        return self.constantTable[cons]

    def getFunctionStartingAddress(self, function: str) -> int:
        '''
        Returns function starting address.
        '''
        if function in self.functionNameMap:
            return self.functionNameMap[function]['address']
        else:
            print(
                f'ERROR: function {function} was not found')
            raise SyntaxError

    def verifyReturnType(self, type: str) -> None:
        '''
        Verifies the return type is the same as the one expected in the function, sets has return flag as true
        '''
        functionReturnType = self.functionNameMap[self.currFunction]['returnType']
        if functionReturnType != type:
            print(
                f'ERROR: return type {type} does not match function return type {functionReturnType}')
            raise SyntaxError
        else:
            self.functionNameMap[self.currFunction]['hasReturn'] = True

    def verifyHasReturn(self) -> None:
        '''
        Verifies the function if not void, had a return statement
        '''
        if not self.functionNameMap[self.currFunction]['hasReturn'] and self.functionNameMap[self.currFunction]['returnType'] != 'void':
            print(
                f'ERROR: function {self.currFunction} has no return statement')
            raise SyntaxError


class SemanticCube(object):
    '''
    Class to keep semantic cube and access it.
    It utilizes a dictornay of dictionaries to access the result in constant O(1) time.
    '''

    def __init__(self) -> None:
        self.cube = {
            "int": {
                "int": {
                    "+": "int",
                    "/": "int",
                    "<": "bool",
                    "=": "int",
                },
                "float": {
                    "+": "float",
                    "/": "float",
                    "<": "bool",
                    "=": "int",
                },
                "char": {
                    "+": "err",
                    "/": "err",
                    "<": "err",
                    "=": "err",
                },
                "bool": {
                    "+": "err",
                    "/": "err",
                    "<": "err",
                    "=": "err",
                },

            },
            "float": {
                "int": {
                    "+": "float",
                    "/": "float",
                    "<": "bool",
                    "=": "float",
                },
                "float": {
                    "+": "float",
                    "/": "float",
                    "<": "bool",
                    "=": "float",
                },
                "char": {
                    "+": "err",
                    "/": "err",
                    "<": "err",
                    "=": "err",
                },
                "bool": {
                    "+": "err",
                    "/": "err",
                    "<": "err",
                    "=": "err",
                },

            },
            "char": {
                "int": {
                    "+": "err",
                    "/": "err",
                    "<": "err",
                    "=": "err",
                },
                "float": {
                    "+": "err",
                    "/": "err",
                    "<": "err",
                    "=": "err",
                },
                "char": {
                    "+": "err",
                    "/": "err",
                    "<": "err",
                    "=": "char",
                },
                "bool": {
                    "+": "err",
                    "/": "err",
                    "<": "err",
                    "=": "err",
                },

            },
            "bool": {
                "int": {
                    "+": "err",
                    "/": "err",
                    "<": "err",
                    "=": "bool",
                },
                "float": {
                    "+": "err",
                    "/": "err",
                    "<": "err",
                    "=": "bool",
                },
                "char": {
                    "+": "err",
                    "/": "err",
                    "<": "err",
                    "=": "err",
                },
                "bool": {
                    "+": "err",
                    "/": "err",
                    "<": "err",
                    "=": "bool",
                },

            },
        }

    def getResult(self, leftOp: str, rightOp: str, symb: str) -> str:
        '''
        Function that given the left, right operator and the symbol returns the semantic result.
        If result is error, a syntax error will be raised.
        '''
        if symb == '-' or symb == '+':
            symb = '+'
        elif symb == '*' or symb == '/':
            symb = '/'
        elif symb == '<' or symb == '>' or symb == '>=' or symb == '<=' or symb == '==' or symb == '!=':
            symb = '<'

        if leftOp in self.cube:
            if rightOp in self.cube[leftOp]:
                if symb in self.cube[leftOp][rightOp]:
                    ans = self.cube[leftOp][rightOp][symb]

                    if ans != 'err':
                        return ans

        print(f'Error: semantic not recognized {leftOp} {symb} {rightOp}')
        raise SyntaxError
