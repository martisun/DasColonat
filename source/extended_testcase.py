import unittest

class ExtendedTestCase(unittest.TestCase):        
    def _assertActualEqualsExpected(self,actual,expected):
        assertion = (actual == expected)
        if not assertion: self.__reportActualAndExpected(actual,expected)
        self.assertTrue(assertion)     
        
    @staticmethod    
    def __reportActualAndExpected(actual,expected):
        print('\nactual:',actual)
        print('expected:',expected)