import unittest
from mock import patch
from source.mocks import MockGUI

import source.write_summary as sw
import source.settings as ss

class whenLoadingInput(unittest.TestCase): 
    def setUp(self):
        self.theGUI = MockGUI()
        
    def _startUpSummaryWriterWithScript(self,script=None):
        self.theGUI.setScript(script)
        sw.SummaryWriter.startUpWithGUI(self.theGUI)
    
    def _assertGUIWasRunWithActionsAndArguments(self,actions,arguments=[]):
        assertion = (self.theGUI.wereActionsCalled(actions) and\
                     self.theGUI.wereArgumentsCalled(arguments))
        self.assertThatIsTrue(assertion)
        
    def assertThatIsTrue(self,assertion):
        if not assertion: self.theGUI.dumpActionsAndArguments()
        super().assertTrue(assertion)
        

class whenSettingIsEmpty(whenLoadingInput):    
    @patch('os.listdir',return_value=[])
    def test_whenInputDirectoryEmptyThenRaiseError(self,patched_os_listdir):
        self.__assertStartUpRaisesNoInputError()
        
    @patch('os.listdir',return_value=['a.dat'])
    def test_whenInputDirectoryWithOneFileNoCSVFileThenRaiseError(self,patched_os_listdir):
        self.__assertStartUpRaisesNoInputError()
    
    @patch('os.listdir',return_value=['a.csv'])
    def test_whenInputDirectoryHasCSVFileThenAskToLoad(self,patched_os_listdir):
        self.theGUI.setScript(True)
        sw.SummaryWriter.startUpWithGUI(self.theGUI)
        self._assertGUIWasRunWithActionsAndArguments('A','a.csv') 
        
    @patch('os.listdir',return_value=['a.csv'])
    def test_whenAnswerToAskToLoadIsNoWhenOnlyOneFileInDirectory(self,patched_os_listdir):
        self._startUpSummaryWriterWithScript(False)
        self._assertGUIWasRunWithActionsAndArguments('AE',['a.csv','NoInputError'])
        
    @patch('os.listdir',return_value=['a.dat','b.dat'])
    def test_whenInputDirectoryWithTwoFilesNoCSVFileThenRaiseError(self,patched_os_listdir):
        self.__assertStartUpRaisesNoInputError()
        
    @patch('os.listdir',return_value=['a.dat','a.csv'])
    def test_whenInputDirectoryWithTwoFilesOneCSVFileThenAskToLoad(self,patched_os_listdir):
        self._startUpSummaryWriterWithScript(True)
        self._assertGUIWasRunWithActionsAndArguments('A','a.csv')  
        
    @patch('os.listdir',return_value=['a.csv','b.csv'])
    def test_whenInputDirectoryWithTwoCSVFilesThenAskToLoadTwice(self,patched_os_listdir):
        self._startUpSummaryWriterWithScript(True)
        self._assertGUIWasRunWithActionsAndArguments('AA',['a.csv','b.csv'])     
    
    def __assertStartUpRaisesNoInputError(self):
        self._startUpSummaryWriterWithScript()
        self._assertGUIWasRunWithActionsAndArguments('E','NoInputError')  

class whenSettingIsNonEmpty(whenLoadingInput):
    def setUp(self):
        super().setUp()
        ss.FilesToLoadFrom = 'a.csv'
    
    @patch('os.listdir',return_value=['a.csv'])
    def test_whenFileInSettingOnlyFileNoQuestionsAsked(self,patched_os_listdir):
        self._startUpSummaryWriterWithScript(False)
        self._assertGUIWasRunWithActionsAndArguments('','')
        
    @patch('os.listdir',return_value=['b.csv'])
    def test_whenFileInSettingNotPresentAskToLoadOtherFile(self,patched_os_listdir):
        self._startUpSummaryWriterWithScript(True)
        self._assertGUIWasRunWithActionsAndArguments('A','b.csv') 
        
    @patch('os.listdir',return_value=[])
    def test_whenFileInSettingButNoFileAskToRemoveFromSettings(self,patched_os_listdir):
        self._startUpSummaryWriterWithScript()
        self._assertGUIWasRunWithActionsAndArguments('ER',['NoInputError','a.csv']) 
        
    @patch('os.listdir',return_value=[])
    def test_whenFileInSettingButNoFileThenRemoveFromSettings(self,patched_os_listdir):
        self._startUpSummaryWriterWithScript(True)
        self.assertThatIsTrue(ss.FilesToLoadFrom is None) 
        
    @patch('os.listdir',return_value=[])
    def test_whenFileInSettingButNoFileThenDontRemoveFromSettings(self,patched_os_listdir):
        self._startUpSummaryWriterWithScript(False)
        self.assertThatIsTrue(ss.FilesToLoadFrom == 'a.csv')     

        