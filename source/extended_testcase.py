import unittest

class ExtendedTestCase(unittest.TestCase):        
    def _assertActualEqualsExpected(self,actual,expected):
        assertion = (actual == expected)
        if not assertion: self.__reportActualAndExpected(actual,expected)
        self.assertTrue(assertion)     

    def __reportActualAndExpected(self,actual,expected):
        if type(actual) == str and type(expected) == str:
            print('Two strings agree up to:')
            i = self.__determineStartIndexLocation(actual,expected)    
            j = self.__determineEndIndexLocation(actual,expected) 
            print('\nactual:',ExtendedTestCase.__addStartAndEndIndicatorsAtPositions(actual,i,j))
            print('expected:',ExtendedTestCase.__addStartAndEndIndicatorsAtPositions(expected,i,j))
        else:
            print('\nactual:',ExtendedTestCase.__getStringRep(actual))
            print('expected:',ExtendedTestCase.__getStringRep(expected))
    
    @staticmethod
    def __determineStartIndexLocation(actual,expected):
        for i in range(-1,len(expected)):
            if i+1 == len(actual) or i+1 == len(expected) or expected[i] != actual[i]: break
        if i == -1: return 0
        else:       return i
        
    @staticmethod 
    def __determineEndIndexLocation(actual,expected):
        j = 0
        for j in range(len(expected)):
            if len(actual) == 0 or expected[len(expected)-j-1] != actual[len(actual)-j-1]:
                break
        return j
    
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