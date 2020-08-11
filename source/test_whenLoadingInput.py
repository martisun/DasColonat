from mock import patch

from source.mock_gui import MockGUIInspector
from source.extended_testcase import ExtendedTestCase

from source.file_loader import FileLoader
from source.mock_file import MockFolderAdapter
from source.settings import Settings

class whenLoadingInput(ExtendedTestCase,MockGUIInspector): 
    def setUp(self):
        self._initializeMockGUI()
        self.theSettings = Settings()
        self.folderAdapter = MockFolderAdapter() 
    
    def _startAndStopFileLoaderWithScript(self,script=None):
        self.theGUI.setScript(script)
        fileLoader = self.__initializeFileLoader()
        fileLoader.getFileToLoadFrom()     
        
    def __initializeFileLoader(self):
        fileLoader = FileLoader()
        fileLoader.setGUITo(self.theGUI)
        fileLoader.setSettingsTo(self.theSettings)
        fileLoader.setFolderAdapterTo(self.folderAdapter)
        return fileLoader
        

class whenFilesToLoadFromSettingIsEmpty(whenLoadingInput):
    def setUp(self):
        super().setUp()
    
    def test00_whenInputDirectoryEmptyThenRaiseError(self):
        self.__assertStartUpRaisesNoInputError()
        
    def test01_whenInputDirectoryWithOneFileNoCSVFileThenRaiseError(self):
        self.folderAdapter.createFileForWriting('a.dat')
        self.__assertStartUpRaisesNoInputError()
    
    def test02_whenInputDirectoryHasCSVFileThenAskToLoad(self):
        self.folderAdapter.createFileForWriting('a.csv')
        self._startAndStopFileLoaderWithScript(True)
        self._assertGUIWasRunWithActionsAndArguments('Al','a.csv') 
        
    def test03_whenAnswerToAskToLoadIsNoWhenOnlyOneFileInDirectory(self):
        self.folderAdapter.createFileForWriting('a.csv')
        self._startAndStopFileLoaderWithScript(False)
        self._assertGUIWasRunWithActionsAndArguments('AlE',['a.csv','NoInputError'])
        
    def test04_whenInputDirectoryWithTwoFilesNoCSVFileThenRaiseError(self):
        self.folderAdapter.createFileForWriting('a.dat')
        self.folderAdapter.createFileForWriting('b.dat')
        self.__assertStartUpRaisesNoInputError()
        
    def test05_whenInputDirectoryWithTwoFilesOneCSVFileThenAskToLoad(self):
        self.folderAdapter.createFileForWriting('a.dat')
        self.folderAdapter.createFileForWriting('a.csv')
        self._startAndStopFileLoaderWithScript(True)
        self._assertGUIWasRunWithActionsAndArguments('Al','a.csv')  
        
    def test06_whenInputDirectoryWithTwoCSVFilesThenAskToLoadTwice(self):
        self.folderAdapter.createFileForWriting('a.csv')
        self.folderAdapter.createFileForWriting('b.csv')
        self._startAndStopFileLoaderWithScript(True)
        self._assertGUIWasRunWithActionsAndArguments('AlAl',['a.csv','b.csv'])     
    
    def __assertStartUpRaisesNoInputError(self):
        self._startAndStopFileLoaderWithScript()
        self._assertGUIWasRunWithActionsAndArguments('E','NoInputError') 
        

class whenFilesToLoadFromSettingIsNonEmpty(whenLoadingInput):
    def setUp(self):
        super().setUp()
        self.theSettings = Settings.setTo({'filesToLoadFrom':['a.csv']})
        self.theSettings.setGUITo(self.theGUI)
    
    def test10_whenFileInSettingOnlyFileNoQuestionsAsked(self):
        self.folderAdapter.createFileForWriting('a.csv')
        self._startAndStopFileLoaderWithScript()
        self._assertGUIWasRunWithActionsAndArguments('','')
        
    def test11_whenFileInSettingNotPresentAskToLoadOtherFile(self):
        self.folderAdapter.createFileForWriting('b.csv')
        self._startAndStopFileLoaderWithScript(True)
        self._assertGUIWasRunWithActionsAndArguments('AlR',['b.csv','a.csv']) 
        
    def test12_whenFileInSettingButNoFileAskToRemoveFromSettings(self):
        self._startAndStopFileLoaderWithScript()
        self._assertGUIWasRunWithActionsAndArguments('ER',['NoInputError','a.csv']) 
        
    def test13_whenFileInSettingButNoFileThenRemoveFromSettings(self):
        self._startAndStopFileLoaderWithScript(True)
        self.assertTrue(not self.theSettings.filesToLoadFrom) 
        
    def test14_whenFileInSettingButNoFileThenDontRemoveFromSettings(self):
        self._startAndStopFileLoaderWithScript(False)
        self.assertTrue(self.theSettings.filesToLoadFrom == ['a.csv'])     

class whenSettingHasMultipleEntries(whenLoadingInput):
    def setUp(self):
        super().setUp()
        self.theSettings = Settings.setTo({'filesToLoadFrom':['a.csv','b.csv']})
        self.theSettings.setGUITo(self.theGUI)
        
    def test21_whenFilesInSettingOnlyFilesNoQuestionsAsked(self):
        self.folderAdapter.createFileForWriting('a.csv')
        self.folderAdapter.createFileForWriting('b.csv')
        self._startAndStopFileLoaderWithScript()
        self._assertGUIWasRunWithActionsAndArguments('','')
        
    def test22_whenFirstFileInSettingAskToRemoveSecond(self):
        self.folderAdapter.createFileForWriting('a.csv')
        self._startAndStopFileLoaderWithScript(True)
        self._assertGUIWasRunWithActionsAndArguments('R','b.csv')     
        
    def test23_whenSecondFileInSettingAskToRemoveFirst(self):
        self.folderAdapter.createFileForWriting('b.csv')
        self._startAndStopFileLoaderWithScript(True)
        self._assertGUIWasRunWithActionsAndArguments('R','a.csv') 
        
    def test24_whenTwoFilesInSettingAskToRemoveBoth(self):
        self._startAndStopFileLoaderWithScript(True)
        self._assertGUIWasRunWithActionsAndArguments('ERR',['NoInputError','a.csv','b.csv']) 
           
