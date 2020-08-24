import unittest

class ExtendedTestCase(unittest.TestCase):        
    def _assertActualEqualsExpected(self,actual,expected):
        assertion = (actual == expected)
        if not assertion: self.__reportActualAndExpected(actual,expected)
        self.assertTrue(assertion)     
        
    @staticmethod    
    def __reportActualAndExpected(actual,expected):
        print('\nactual:',ExtendedTestCase.__getStringRep(actual))
        print('expected:',ExtendedTestCase.__getStringRep(expected))
        
    @staticmethod
    def __getStringRep(objectToPrint):
        printRepOfObject = str(objectToPrint)
        printRepOfObject = printRepOfObject.replace('\t','\\t')
        printRepOfObject = printRepOfObject.replace('\r','\\r')
        return printRepOfObject.replace('\b','\\b')