from copy import deepcopy
import sys


class VariablesAddress(object):
    '''
    Class to keep addresses of variables.
    '''

    def __init__(self) -> None:
        self.addressDictDefault = {
            'global': {
                "int": 0,
                "float": 250,
                "char": 500,
                "bool": 750,
            },
            'local': {
                "int": 1000,
                "float": 1250,
                "char": 1500,
                "bool": 1750,
                "temporal": 2000
            },
            'constant': {
                "int": 2250,
                "float": 2500,
                "char": 2750,
                "bool": 3000,
                "string": 3250
            },

        }
        self.addressDict = deepcopy(self.addressDictDefault)
        self.currentScope = 'global'

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
        Returns the variable type, scope and starting address depending on the address given.
        '''
        lastType = 'int'
        lastScope = 'global'

        for scope in self.addressDict.keys():
            for types in self.addressDict[scope].keys():
                if address <= self.addressDict[scope][types]:
                    if address == self.addressDict[scope][types]:
                        return (scope, types, self.addressDictDefault[scope][types])
                    else:
                        return (lastScope, lastType, self.addressDictDefault[lastScope][lastType])
                else:
                    lastType = types
                    lastScope = scope

        sys.exit(f'Error: address not found')

    def setCurrentScope(self, scope: str) -> None:
        '''
        Sets the current scope to the given parameter.
        '''
        if scope in self.addressDictDefault.keys():
            self.currentScope = scope
        else:
            sys.exit(f'Error: scope {scope} name not found')

    def resetScope(self, scope: str) -> None:
        '''
        Resets the given scope with the default values.
        '''
        if scope in self.addressDict.keys():
            self.addressDict[scope] = deepcopy(self.addressDictDefault[scope])
        else:
            sys.exit(f'Error: scope {scope} name not found')
