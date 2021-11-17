from parser.quadruples import Quadruples
from parser.variable_semantics import FunctionTable
import json


class ObjectFile(object):
    '''
    Class to create and write quadruples, 
    function table and constants to an object file.
    '''

    def __init__(self, quads: Quadruples, table: FunctionTable) -> None:
        self.quads = quads
        self.table = table

    def create(self):
        '''
        Function to create the object file.
        '''
        with open("obj.json", "w") as f:
            obj = {
                'functionTable': self.table.getFunctions(),
                'constantTable': self.table.getConstants(),
                'quads': self.quads.getQuads()
            }
            json.dump(obj, f)

    def print(self):
        '''
        Function to print the object file.
        '''
        print(self.table.getFunctions())
        print(self.table.getConstants())
        self.quads.printQuad()
