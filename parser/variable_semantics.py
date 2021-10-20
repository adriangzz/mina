
class FunctionTable(object):
    '''
    Class to keep variable semantics.
    Created using a dictionary of dictionaries that stores the names of the functions as keys for O(N) search time
    and the rest of the values as a dictionary. e.j. {'funcName':{'name':'funcName','type':'int',...}}.
    Stores the latest added function name to add all the next variables to that scope.
    Variables are added to a new table added as a value to the function dictionary.
    '''

    def __init__(self) -> None:
        self.funcNameMap = {}
        self.currFunction = ''
        self.programName = ''
        self.currType = ''

    def addFunction(self, row: dict) -> None:
        '''
        Checks name of function does not exist, then adds it to the dictionary using it's name as key.
        Sets current function as this function.
        Raises syntaxerror if function already exists.
        '''
        if row['name'] not in self.funcNameMap:
            self.funcNameMap[row['name']] = row
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
        if name and name in self.funcNameMap and row['name'] not in self.funcNameMap[name]['variables']:
            self.funcNameMap[name]['variables'][row['name']] = row
        elif row['name'] not in self.funcNameMap[self.currFunction]['variables']:
            self.funcNameMap[self.currFunction]['variables'][row['name']] = row
        else:
            print(row, self.currFunction, self.currType,
                  self.funcNameMap[self.currFunction])
            print("Error: variable name already in use")
            raise SyntaxError

    def getFunction(self, name: str) -> dict:
        '''
        Function that returns the dictionary of the name of function given.
        Returns empty dict if name does not exist.
        '''
        if name in self.funcNameMap:
            return self.funcNameMap[name]
        return {}

    def getFunctions(self) -> dict:
        '''
        Returns the whole dictionary of functions and variables.
        '''
        return self.funcNameMap

    def deleteFunction(self, name: str) -> bool:
        '''
        Deletes function given the name.
        Returns true if deleted, false otherwise.
        '''
        if name in self.funcNameMap:
            self.funcNameMap.pop(name)
            return True
        return False

    def functionExists(self, name: str) -> bool:
        '''
        Returns true if function exists in table, false otherwise.
        '''
        return name in self.funcNameMap

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

    def checkVariableExists(self, name: str) -> None:
        '''
        Checks if variable is declared, raises syntax error if not.
        '''
        if name not in self.funcNameMap[self.currFunction]['variables'] and name not in self.funcNameMap[self.programName]['variables']:
            print(self.currFunction, self.programName,
                  self.funcNameMap[self.currFunction]['variables'])
            print(
                f'Error: variable {name} not declared in scope or global variables')
            raise SyntaxError
