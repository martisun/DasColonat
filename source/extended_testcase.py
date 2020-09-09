import unittest

class ExtendedTestCase(unittest.TestCase):        
    def _assertActualEqualsExpected(self,actual,expected):
        assertion = (actual == expected)
        if not assertion: self.__reportActualAndExpected(actual,expected)
        self.assertTrue(assertion)     
        
    @staticmethod    
    def __reportActualAndExpected(actual,expected):
        if type(actual) == str and type(expected) == str:
            print('Two strings agree up to:')
            startString = ''
            for i in range(len(expected)):
                if expected[i] != actual[i]: 
                    startString = expected[:i]+'-->|'
                    break
            for j in range(len(expected)):
                if expected[len(expected)-j-1] != actual[len(actual)-j-1]:
                    endString = '|<--'+expected[(len(expected)-j-1):]
                    break
            expectedMiddleString = expected[i:(len(expected)-j)]
            actualMiddleString   = actual[i:(len(actual)-j)]
            print('\nactual:',ExtendedTestCase.__getStringRep(startString+actualMiddleString\
                                                              +endString))
            print('expected:',ExtendedTestCase.__getStringRep(startString+expectedMiddleString\
                                                              +endString))
        else:
            print('\nactual:',ExtendedTestCase.__getStringRep(actual))
            print('expected:',ExtendedTestCase.__getStringRep(expected))
                      
    @staticmethod
    def __getStringRep(objectToPrint):
        printRepOfObject = str(objectToPrint)
        printRepOfObject = printRepOfObject.replace('\t','\\t')
        printRepOfObject = printRepOfObject.replace('\r','\\r')
        return printRepOfObject.replace('\b','\\b')