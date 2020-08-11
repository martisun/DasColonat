import builtins
from mock import patch

from source.settings import Settings
from source.task_manager import TaskManager
from source.phrases_factory import PhrasesFactory

from source.mock_gui import MockGUI
from source.mock_file import MockFolderAdapter
from source.test_whenUsingMockFile import whenUsingMockFile

class whenCheckingAgainstGoldStandard(whenUsingMockFile):
    def setUp(self):
        self.folderAdapter = MockFolderAdapter() 
        with self.folderAdapter.open('baptism.csv','w') as fileObject:
            fileObject.write(GOLD_INPUT)
        self.theSettings = Settings.setTo(GOLD_SETTINGS) 
        self.fileObject = fileObject    
    
    def test_whenGoldInputIsSet(self):
        self._assertThatFileContentEquals(GOLD_INPUT)
    
    def test_whenAfterGUIProcessingThenOutputIsGold(self):
        content = self._readContentFromFileWithName('baptism.csv')    
        self._writeContentToFileWithName(content,'summary.tex')
        self.__assertThatFileWithNameHasGoldStandard('summary.tex')
        
    def __assertThatFileWithNameHasGoldStandard(self,fileName):
        content = self._readContentFromFileWithName(fileName)
        self._assertActualEqualsExpected(content,GOLD_INPUT)
    
class whenReadingAndWritingWithTaskManager(whenUsingMockFile):
    def setUp(self):
        self.folderAdapter = MockFolderAdapter()
        self.theGUI = MockGUI()
        self.taskManager = TaskManager()
        self.taskManager.setGUITo(self.theGUI)
        self.taskManager.setFolderAdapterTo(self.folderAdapter)
        self.theSettings = Settings.setTo(GOLD_SETTINGS)
    
    def test_useTaskManagerForProcessingDifferentInputFiles(self):
        for inputFileName in ['a.csv','b.csv','c.csv']:
            with self.subTest(inputFileName=inputFileName):
                self.__useFileLoaderForProcessingGoldWithIOFileNames(inputFileName,'summary.tex')
                
    def test_useTaskManagerForProcessingDifferentOutputFiles(self):
        for outputFileName in ['a.tex','b.tex','c.tex']:
            with self.subTest(outputFileName=outputFileName):
                self.__useFileLoaderForProcessingGoldWithIOFileNames('baptism.csv',outputFileName)   
                
    def test_useLanguageSettings(self):
        for language in ['en','nl','de']:
            with self.subTest(language=language):
                self.__useLanguageInSettings(language)            
                
    def test_useTaskManagerForProcessingGold(self):
        self.__useFileLoaderForProcessingGoldWithIOFileNames('baptism.csv','summary.tex')
        
    def __useLanguageInSettings(self,tag):
        self.__writeGoldInputToFileWithName('baptism.csv')
        self.__setGoldSettingsWithUpdate({'language':tag})
        self.taskManager.run()
        actual = self._readContentFromFileWithName('summary.tex')
        expected = self.__getGoldOutputInLanguage(tag)
        self._assertActualEqualsExpected(actual,expected)         
        
    def __useFileLoaderForProcessingGoldWithIOFileNames(self,inputFileName,outputFileName):
        self.__writeGoldInputToFileWithName(inputFileName)
        self.__setGoldSettingsWithUpdate({'filesToLoadFrom':[inputFileName],\
                                           'filesToSaveTo':outputFileName})
        self.taskManager.run()
        actual   = self._readContentFromFileWithName(outputFileName)
        expected = self.__getGoldOutputInLanguage('en')
        self._assertActualEqualsExpected(actual,expected)
        
    def __setGoldSettingsWithUpdate(self,updateDict):
        self.theSettings.updateWith(updateDict)
        self.taskManager.setSettingsTo(self.theSettings)

    def __writeGoldInputToFileWithName(self,fileName):
        self._writeContentToFileWithName(GOLD_INPUT,fileName)
    
    @staticmethod
    def __getGoldOutputInLanguage(tag):
        phrases = PhrasesFactory.inLanguage(tag)
        return GOLD_INPUT%phrases
    
GOLD_SETTINGS = {'filesToLoadFrom':['baptism.csv'],\
                 'filesToSaveTo':'summary.tex'}
    
GOLD_INPUT = """
\section{\pidt{(Fr0)}-- Sunder, Jois --~\Mars}\label{sec:(Fr0)}

%s Jois \textbf{S}under\pids{(Fr0)} %s Alheid \pids{x1(Fr0)} %s: 
\begin{itemize}
\item[\emph{\rom{1}.}] Wolterus~(\textbf{?})~\pids{(Fr0.1)} %s 18%s 1661 %s {\it St. Vitus} %s Freren.   
\end{itemize} 
"""