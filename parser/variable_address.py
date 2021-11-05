class VariablesAddress(object):
    '''
    Class to keep addresses of variables.
    '''

    def __init__(self) -> None:
        self.addressDictDefault = {
            'globalVariable': {
                "int": 1000,
                "float": 4000,
                "char": 6000,
                "bool": 9000,
            },
            'localVariable': {
                "int": 10000,
                "float": 14000,
                "char": 16000,
                "bool": 19000,
            },
            'temporalVariable': {
                "int": 20000,
                "float": 24000,
                "char": 26000,
                "bool": 29000,
            },
            'constant': {
                "int": 30000,
                "float": 34000,
                "char": 36000,
                "bool": 39000,
            }

        }
        self.addressDict = self.addressDictDefault.copy()
        self.currentScope = 'globalVariable'

    def getTypeStartingAddress(self, scope: str, type: str) -> int:
        '''
        Get the next available address depending on the scope and type.
        '''
        if scope in self.addressDictDefault:
            if type in self.addressDictDefault[scope]:
                address = self.addressDict[scope][type]
                self.addressDict[scope][type] += 1
                return address

    def getType(self, address: int) -> tuple:
        '''
        Returns the variable type and scope depending on the address given.
        '''
        lastType = 'int'
        lastScope = 'globalVariable'

        for scope in self.addressDict.keys():
            for types in self.addressDict[scope].keys():
                if address <= self.addressDict[scope][types]:
                    if address == self.addressDict[scope][types]:
                        return (scope, types)
                    else:
                        return (lastScope, lastType)
                else:
                    lastType = types
                    lastScope = scope

        print(f'Error: address not found')
        raise SyntaxError

    def setCurrentScope(self, scope: str) -> None:
        if scope in self.addressDictDefault.keys():
            self.currentScope = scope
        else:
            print(f'Error: scope name not found')
            raise SyntaxError

    def resetScope(self, scope: str) -> None:
        '''
        Resets the given scope with the default values.
        '''
        if scope in self.addressDict.keys():
            self.addressDict[scope] = self.addressDictDefault[scope].copy()
        else:
            print(f'Error: scope name not found')
            raise SyntaxError
