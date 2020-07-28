from mock import patch

from source.mock_gui import MockGUI
from source.extended_testcase import ExtendedTestCase

from source.file_loader import FileLoader
from source.settings import Settings

class whenLoadingInput(ExtendedTestCase): 
    def setUp(self):
        self._spyObject = MockGUI()
        self.theSettings = Settings({'filesToLoadFrom':[]})      
        
    def _startUpFileLoaderWithScript(self,script=None):
        self._spyObject.setScript(script)
        fileLoader = self.__initializeFileLoader()
        fileLoader.startUp()
        
    def _assertGUIWasRunWithActionsAndArguments(self,actions,arguments=[]):
        self._assertSpyWasRunWithActionsAndArguments(actions,arguments)
        
    def __initializeFileLoader(self):
        fileLoader = FileLoader()
        fileLoader.setGUITo(self._spyObject)
        fileLoader.setSettingsTo(self.theSettings)
        return fileLoader
        

class whenSettingIsEmpty(whenLoadingInput):
    def setUp(self):
        super().setUp()
    
    @patch('os.listdir',return_value=[])
    def test_whenInputDirectoryEmptyThenRaiseError(self,patched_os_listdir):
        self.__assertStartUpRaisesNoInputError()
        
    @patch('os.listdir',return_value=['a.dat'])
    def test_whenInputDirectoryWithOneFileNoCSVFileThenRaiseError(self,patched_os_listdir):
        self.__assertStartUpRaisesNoInputError()
    
    @patch('os.listdir',return_value=['a.csv'])
    def test_whenInputDirectoryHasCSVFileThenAskToLoad(self,patched_os_listdir):
        self._startUpFileLoaderWithScript(True)
        self._assertGUIWasRunWithActionsAndArguments('A','a.csv') 
        
    @patch('os.listdir',return_value=['a.csv'])
    def test_whenAnswerToAskToLoadIsNoWhenOnlyOneFileInDirectory(self,patched_os_listdir):
        self._startUpFileLoaderWithScript(False)
        self._assertGUIWasRunWithActionsAndArguments('AE',['a.csv','NoInputError'])
        
    @patch('os.listdir',return_value=['a.dat','b.dat'])
    def test_whenInputDirectoryWithTwoFilesNoCSVFileThenRaiseError(self,patched_os_listdir):
        self.__assertStartUpRaisesNoInputError()
        
    @patch('os.listdir',return_value=['a.dat','a.csv'])
    def test_whenInputDirectoryWithTwoFilesOneCSVFileThenAskToLoad(self,patched_os_listdir):
        self._startUpFileLoaderWithScript(True)
        self._assertGUIWasRunWithActionsAndArguments('A','a.csv')  
        
    @patch('os.listdir',return_value=['a.csv','b.csv'])
    def test_whenInputDirectoryWithTwoCSVFilesThenAskToLoadTwice(self,patched_os_listdir):
        self._startUpFileLoaderWithScript(True)
        self._assertGUIWasRunWithActionsAndArguments('AA',['a.csv','b.csv'])     
    
    def __assertStartUpRaisesNoInputError(self):
        self._startUpFileLoaderWithScript()
        self._assertGUIWasRunWithActionsAndArguments('E','NoInputError')  

class whenSettingIsNonEmpty(whenLoadingInput):
    def setUp(self):
        super().setUp()
        self.theSettings = Settings({'filesToLoadFrom':['a.csv']})
    
    @patch('os.listdir',return_value=['a.csv'])
    def test_whenFileInSettingOnlyFileNoQuestionsAsked(self,patched_os_listdir):
        self._startUpFileLoaderWithScript()
        self._assertGUIWasRunWithActionsAndArguments('','')
        
    @patch('os.listdir',return_value=['b.csv'])
    def test_whenFileInSettingNotPresentAskToLoadOtherFile(self,patched_os_listdir):
        self._startUpFileLoaderWithScript(True)
        self._assertGUIWasRunWithActionsAndArguments('AR',['b.csv','a.csv']) 
        
    @patch('os.listdir',return_value=[])
    def test_whenFileInSettingButNoFileAskToRemoveFromSettings(self,patched_os_listdir):
        self._startUpFileLoaderWithScript()
        self._assertGUIWasRunWithActionsAndArguments('ER',['NoInputError','a.csv']) 
        
    @patch('os.listdir',return_value=[])
    def test_whenFileInSettingButNoFileThenRemoveFromSettings(self,patched_os_listdir):
        self._startUpFileLoaderWithScript(True)
        self.assertThatIsTrue(not self.theSettings.filesToLoadFrom) 
        
    @patch('os.listdir',return_value=[])
    def test_whenFileInSettingButNoFileThenDontRemoveFromSettings(self,patched_os_listdir):
        self._startUpFileLoaderWithScript(False)
        self.assertThatIsTrue(self.theSettings.filesToLoadFrom == ['a.csv'])     

class whenSettingHasMultipleEntries(whenLoadingInput):
    def setUp(self):
        super().setUp()
        self.theSettings = Settings({'filesToLoadFrom':['a.csv','b.csv']})
        
    @patch('os.listdir',return_value=['a.csv','b.csv'])
    def test_whenFilesInSettingOnlyFilesNoQuestionsAsked(self,patched_os_listdir):
        self._startUpFileLoaderWithScript()
        self._assertGUIWasRunWithActionsAndArguments('','')
        
    @patch('os.listdir',return_value=['a.csv'])
    def test_whenFirstFileInSettingAskToRemoveSecond(self,patched_os_listdir):
        self._startUpFileLoaderWithScript(True)
        self._assertGUIWasRunWithActionsAndArguments('R','b.csv')     
        
    @patch('os.listdir',return_value=['b.csv'])
    def test_whenSecondFileInSettingAskToRemoveFirst(self,patched_os_listdir):
        self._startUpFileLoaderWithScript(True)
        self._assertGUIWasRunWithActionsAndArguments('R','a.csv') 
        
    @patch('os.listdir',return_value=[])
    def test_whenTwoFilesInSettingAskToRemoveBoth(self,patched_os_listdir):
        self._startUpFileLoaderWithScript(True)
        self._assertGUIWasRunWithActionsAndArguments('ERR',['NoInputError','a.csv','b.csv']) 
           
