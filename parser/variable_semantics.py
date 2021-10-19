
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

    def addFunc(self, row) -> bool:
        if row['name'] not in self.funcNameMap:
            self.funcNameMap[row['name']] = row
            self.currFunc = row['name']
            return True
        return False

    def getFunc(self, name) -> dict:
        if name in self.funcNameMap:
            return self.funcNameMap[name]
        return {}

    def deleteFunc(self, name) -> None:
        if name in self.funcNameMap:
            self.funcNameMap.pop(name)

    def funcExists(self, name) -> bool:
        return name in self.funcNameMap


table = FunctionTable()
print(table.addFunc({'name': 'a', 'type': 'int'}))
print(table.addFunc({'name': 'a', 'type': 'int'}))
print(table.getFunc('int'))
print(table.funcExists('a'))
print(table.deleteFunc('a'))
print(table.funcExists('a'))
