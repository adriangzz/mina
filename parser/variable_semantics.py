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
        self.currFunction = ''
        self.programName = ''
        self.currType = ''

    def addFunction(self, row: dict) -> None:
        '''
        Checks name of function does not exist, then adds it to the dictionary using it's name as key.
        Sets current function as this function.
        Raises syntaxerror if function already exists.
        '''
        if row['name'] not in self.functionNameMap:
            self.functionNameMap[row['name']] = row
            self.currFunction = row['name']
        else:
            print("Error: function name already in use")
            raise SyntaxError

    def addVariables(self, row: dict, name: str = None) -> bool:
        '''
        Function to add variables to current function.
        Uses last added function as default, but an extra optional parameter with the name of the function is accepted.
        Returns true if variables were added, false otherwise.
        '''
        if name and name in self.functionNameMap and row['name'] not in self.functionNameMap[name]['variables']:
            self.functionNameMap[name]['variables'][row['name']] = row
        elif row['name'] not in self.functionNameMap[self.currFunction]['variables']:
            self.functionNameMap[self.currFunction]['variables'][row['name']] = row
        else:
            print("Error: variable name '" +
                  row['name'] + "' already in use")
            raise SyntaxError

    def getFunction(self, name: str) -> dict:
        '''
        Function that returns the dictionary of the name of function given.
        Returns empty dict if name does not exist.
        '''
        if name in self.functionNameMap:
            return self.functionNameMap[name]
        return {}

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

    def deleteFunctionVariables(self, name: str) -> bool:
        '''
        Deletes function given the name.
        Returns true if deleted, false otherwise.
        '''
        if name in self.functionNameMap:
            self.functionNameMap[name].pop('variables')
            return True
        return False

    def functionExists(self, name: str) -> bool:
        '''
        Returns true if function exists in table, false otherwise.
        '''
        return name in self.functionNameMap

    def setCurrentFunction(self, name: str) -> None:
        '''
        Sets current function.
        '''
        self.currFunction = name

    def getCurrentFunction(self) -> str:
        '''
        Gets current function.
        '''
        return self.currFunction

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

    def checkVariableExists(self, name: str) -> None:
        '''
        Checks if variable is declared, raises syntax error if not.
        '''
        if name not in self.functionNameMap[self.currFunction]['variables'] and name not in self.functionNameMap[self.programName]['variables']:
            print(
                f'Error: variable {name} not declared in scope or global variables')
            raise SyntaxError

    def deleteTable(self) -> None:
        '''
        Deletes table.
        '''
        del self.functionNameMap


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
                },
                "float": {
                    "+": "float",
                    "/": "float",
                    "<": "bool",
                },
                "char": {
                    "+": "err",
                    "/": "err",
                    "<": "err",
                },

            },
            "float": {
                "int": {
                    "+": "float",
                    "/": "float",
                    "<": "bool",
                },
                "float": {
                    "+": "float",
                    "/": "float",
                    "<": "bool",
                },
                "char": {
                    "+": "err",
                    "/": "err",
                    "<": "err",
                },

            },
            "char": {
                "int": {
                    "+": "err",
                    "/": "err",
                    "<": "err",
                },
                "float": {
                    "+": "err",
                    "/": "err",
                    "<": "err",
                },
                "char": {
                    "+": "err",
                    "/": "err",
                    "<": "err",
                },

            },
        }

    def getResult(self, leftOp: str, rightOp: str, symb: str) -> str:
        '''
        Function that given the left, right operator and the symbol returns the semantic result.
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

        print(f'Error: semantic not recognized')
        raise SyntaxError
