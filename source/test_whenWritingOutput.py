import builtins
from mock import patch

from source.extended_testcase import ExtendedTestCase
from source.mock_file import MockFile

class whenFileCreated(ExtendedTestCase): 
    @patch('builtins.open',return_value=MockFile.open('a.txt','w'))
    def setUp(self,patched_open):
        self._spyObject = open('a.txt','w')
    
    def test_outputEqualsEmptyInput(self):
        self.__assertThatReadOutputEquals('')
        
    def test_outputEqualsNonEmptyInput(self):
        self._spyObject.write('a')
        self.__assertThatReadOutputEquals('a')
        
    def test_whenWriteThenOpenedWithPermission(self):
        self._assertFileWasRunWithActionsAndArguments('O',[['a.txt','w']]) 
        
    def __assertThatReadOutputEquals(self,content):
        self.assertTrue(self._spyObject.read() == content)
        
    def _assertFileWasRunWithActionsAndArguments(self,actions,arguments=[]):
        self._assertSpyWasRunWithActionsAndArguments(actions,arguments)       