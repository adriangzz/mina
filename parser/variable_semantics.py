from parser.variable_address import VariablesAddress
import sys


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
        self.constantTable = {'size': {}, 'vars': {}}
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
            sys.exit("Error: function name already in use")

    def addVariables(self, row: dict, name: str = None, size: int = 1) -> None:
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
            sys.exit("Error: variable name '" +
                     row['name'] + "' already in use")

        self.addSize(row['type'], size)

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
            sys.exit(
                f'Error: function {function} only takes {paramCount} arguments')

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

    def addSize(self, type: str, size: int = 1) -> None:
        '''
        Adds size given or 1 to current function size.
        '''
        if type in self.functionNameMap[self.currFunction]['size']:
            self.functionNameMap[self.currFunction]['size'][type] += size
        else:
            self.functionNameMap[self.currFunction]['size'][type] = size

    def getFunctions(self) -> dict:
        '''
        Returns the whole dictionary of functions and variables.
        '''
        return self.functionNameMap

    def getConstants(self) -> dict:
        '''
        Returns the whole dictionary of constants.
        '''
        return self.constantTable

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
            sys.exit(f'Error: function {name} not declared')

    def functionExists(self, name: str) -> None:
        '''
        Raises syntax error if funciton does not exist.
        '''
        if name not in self.functionNameMap:
            sys.exit(f'Error: function {name} not declared')

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

    def getFuncitonSize(self, name: str) -> dict:
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
        sys.exit(
            f'Error: variable {name} not declared in scope or global variables')

    def getGlobalVariable(self, name: str) -> dict:
        '''
        Returns the given function global variable.
        '''
        if name in self.functionNameMap[self.programName]['variables']:
            return self.functionNameMap[self.programName]['variables'][name]
        sys.exit(
            f'Error: variable {name} not declared in scope or global variables')

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
        return cons in self.constantTable['vars']

    def addConstant(self, cons: any, address: int, type: str) -> None:
        '''
        Adds constant to table.
        '''
        self.constantTable['vars'][cons] = (address, type)
        if type in self.constantTable['size']:
            self.constantTable['size'][type] += 1
        else:
            self.constantTable['size'][type] = 1

    def getConstant(self, cons: any) -> int:
        '''
        Returns constant address.
        '''
        return self.constantTable['vars'][cons][0]

    def getFunctionStartingAddress(self, function: str) -> int:
        '''
        Returns function starting address.
        '''
        if function in self.functionNameMap:
            return self.functionNameMap[function]['address']
        else:
            sys.exit(
                f'ERROR: function {function} was not found')

    def verifyReturnType(self, type: str) -> None:
        '''
        Verifies the return type is the same as the one expected in the function, sets has return flag as true
        '''
        functionReturnType = self.functionNameMap[self.currFunction]['returnType']
        if functionReturnType != type:
            sys.exit(
                f'ERROR: return type {type} does not match function return type {functionReturnType}')
        else:
            self.functionNameMap[self.currFunction]['hasReturn'] = True

    def verifyHasReturn(self) -> None:
        '''
        Verifies the function if not void, had a return statement
        '''
        if not self.functionNameMap[self.currFunction]['hasReturn'] and self.functionNameMap[self.currFunction]['returnType'] != 'void':
            sys.exit(
                f'ERROR: function {self.currFunction} has no return statement')

    def setFunctionMap(self, map: dict) -> None:
        '''
        Function to set the function map from one previously created.
        '''
        self.functionNameMap = map

    def setConstantTable(self, map: dict) -> None:
        '''
        Function to set the constant table from one previously created.
        '''
        self.constantTable = map


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
                    "&": "bool",
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
                    "&": "bool",
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
                    "&": "bool",
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
                    "&": "bool",
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
        elif symb == '&' or symb == '|':
            symb = '&'

        if leftOp in self.cube:
            if rightOp in self.cube[leftOp]:
                if symb in self.cube[leftOp][rightOp]:
                    ans = self.cube[leftOp][rightOp][symb]

                    if ans != 'err':
                        return ans

        sys.exit(f'Error: semantic not recognized {leftOp} {symb} {rightOp}')
