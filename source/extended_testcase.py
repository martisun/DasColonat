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
            for i in range(len(expected)):
                if expected[i] != actual[i]: break
            for j in range(len(expected)):
                if expected[len(expected)-j-1] != actual[len(actual)-j-1]: break
            print('\nactual:',ExtendedTestCase.__addStartAndEndIndicatorsAtPositions(actual,i,j))
            print('expected:',ExtendedTestCase.__addStartAndEndIndicatorsAtPositions(expected,i,j))
        else:
            print('\nactual:',ExtendedTestCase.__getStringRep(actual))
            print('expected:',ExtendedTestCase.__getStringRep(expected))
                      
    @staticmethod
    def __addStartAndEndIndicatorsAtPositions(string,i,j):
        startIndicator = '-->|'
        endIndicator   = '|<--'
        jFromFront = (len(string)-j)
        if i < jFromFront:
            return ExtendedTestCase.__getStringRep(string[:i]+startIndicator\
                      +string[i:jFromFront]+endIndicator+string[jFromFront:])
        else:
            return ExtendedTestCase.__getStringRep(string[:jFromFront]\
                      +endIndicator+string[jFromFront:i]+startIndicator+string[i:])
    
    
    @staticmethod
    def __getStringRep(objectToPrint):
        printRepOfObject = str(objectToPrint)
        printRepOfObject = printRepOfObject.replace('\t','\\t')
        printRepOfObject = printRepOfObject.replace('\r','\\r')
        return printRepOfObject.replace('\b','\\b')