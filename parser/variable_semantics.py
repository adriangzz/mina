
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
        self.currFunc = ''

    def addFunction(self, row: dict) -> bool:
        '''
        Checks name of function does not exist, then adds it to the dictionary using it's name as key.
        Sets current function as this function.
        Returns true if added, otherwise false.
        '''
        if row['name'] not in self.funcNameMap:
            self.funcNameMap[row['name']] = row
            self.currFunc = row['name']
            return True
        return False

    def addVariables(self, row: dict, name: str = None) -> bool:
        '''
        Function to add variables to current function.
        Uses last added function as default, but an extra optional parameter with the name of the function is accepted.
        Returns true if variables were added, false otherwise.
        '''
        if name and name in self.funcNameMap and row['name'] not in self.funcNameMap[name]['variables']:
            self.funcNameMap[name]['variables'][row['name']] = row
            return True
        else:
            if row['name'] not in self.funcNameMap[self.currFunc]['variables']:
                self.funcNameMap[self.currFunc]['variables'][row['name']] = row
                return True
        return False

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


table = FunctionTable()
table.addFunction({'name': 'adrian', 'variables': {}})
table.addFunction({'name': 'david', 'variables': {}})
table.addVariables({'name': 'a', 'type': 'int'})
table.addVariables({'name': 'b', 'type': 'float'})
print(table.addVariables({'name': 'a', 'type': 'string'}, "d"))
print(table.getFunctions())
