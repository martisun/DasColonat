import builtins
from mock import patch

from source.settings import Settings
from source.task_manager import TaskManager
from source.summary_writer import SummaryWriter
from source.phrase_writer import PhraseWriter

from source.mock_gui import MockGUI
from source.mock_file import MockFolderAdapter
from source.test_whenUsingMockFile import whenUsingMockFile
from source.test_whenUsingFileParser import STR_INPUT
from source.test_whenUsingEnglishPhraseWriter import FATHER_INPUT,MOTHER_INPUT

class whenCheckingAgainstGoldStandard(whenUsingMockFile):
    def setUp(self):
        self.folderAdapter = MockFolderAdapter()
        with self.folderAdapter.open('baptism.csv','w') as fileObject:
            fileObject.write(FATHER_INPUT)
        self.theSettings = Settings.setTo(GOLD_SETTINGS) 
        self.fileObject = fileObject    
    
    def test_whenGoldInputIsSet(self):
        self._assertThatFileContentEquals(FATHER_INPUT)
    
    def test_whenAfterGUIProcessingThenOutputIsGold(self):
        content = self._readContentFromFileWithName('baptism.csv')    
        self._writeContentToFileWithName(content,'summary.tex')
        self.__assertThatFileWithNameHasGoldStandard('summary.tex')
        
    def __assertThatFileWithNameHasGoldStandard(self,fileName):
        content = self._readContentFromFileWithName(fileName)
        self._assertActualEqualsExpected(content,FATHER_INPUT)
    
class whenReadingAndWritingWithTaskManager(whenUsingMockFile):
    def setUp(self):
        self.folderAdapter = MockFolderAdapter()
        self.theGUI = MockGUI()
        self.taskManager = TaskManager()
        self.taskManager.setGUITo(self.theGUI)
        self.taskManager.setFolderAdapterTo(self.folderAdapter)
        self.theSettings = Settings.setTo(GOLD_SETTINGS)
        self.__template  = FATHER_INPUT 
    
    def test_useTaskManagerForProcessingDifferentInputFiles(self):
        """Tests whether it is possible to use an input file with
        different names. By setting the name of the file to 
        'filesToLoadFrom' in the used settings."""
        for inputFileName in ['a.csv','b.csv','c.csv']:
            with self.subTest(inputFileName=inputFileName):
                self.__useTaskManagerToFillTemplateWithIOFileNames(inputFileName,'summary.tex')
                
    def test_useTaskManagerForProcessingDifferentOutputFiles(self):
        """Tests whether it is possible to specify the name
        of the file wherein the output is written by setting
        the name in 'filesToSaveTo' in the used settings."""
        for outputFileName in ['a.tex','b.tex','c.tex']:
            with self.subTest(outputFileName=outputFileName):
                self.__useTaskManagerToFillTemplateWithIOFileNames('baptism.csv',outputFileName)   
                
    def test_useLanguageSettings(self):
        """Tests whether it is possible to specify the name
        of the language wherein the output is written by setting
        a tag in 'language' in the used settings."""
        for language in ['en','nl','de']:
            with self.subTest(language=language):
                self.__useLanguageInSettings(language)            
                
    def test_templateRelativeToFatherInBaptismRecord(self):
        """Tests whether the output adheres to a predefined
        template when requesting a summary for the father
        of a single baptism record."""
        self.__useTaskManagerToFillTemplateWithIOFileNames('baptism.csv','summary.tex')
        
    def test_templateRelativeToMotherInBaptismRecord(self):
        """Tests whether the output adheres to a predefined
        template when requesting a summary for the mother
        of a single baptism record."""
        self.__template  = MOTHER_INPUT 
        self.__useTaskManagerToFillTemplateWithIOFileNames('baptism.csv','summary.tex','mother')
    
    def __useLanguageInSettings(self,tag):
        self.__writeTemplateToFileWithName('baptism.csv')
        self.__setTaskManagerSettingsWithUpdate({'language':tag})
        self.__assertTaskManagerOutputEqualsContentOfFileWithName('summary.tex')       
        
    def __useTaskManagerToFillTemplateWithIOFileNames(self,inputFileName,outputFileName,
                                                      roleOfMain='father'):
        self.__writeTemplateToFileWithName(inputFileName)
        self.__setTaskManagerSettingsWithUpdate({'filesToLoadFrom':[inputFileName],
                                                 'filesToSaveTo':outputFileName,
                                                 'roleOfMain':roleOfMain})
        self.__assertTaskManagerOutputEqualsContentOfFileWithName(outputFileName)
        
    def __assertTaskManagerOutputEqualsContentOfFileWithName(self,outputFileName):    
        self.taskManager.run()
        actual   = self._readContentFromFileWithName(outputFileName)
        expected = self.__getOutputSummaryInLanguage()
        self._assertActualEqualsExpected(actual,expected)
        
    def __getOutputSummaryInLanguage(self):
        summaryWriter = SummaryWriter()
        phraseWriter = self.theSettings.getPhraseWriter()
        summaryWriter.setPhraseWriterTo(phraseWriter)        
        summaryWriter.setPeopleTo(self.__template)
        return summaryWriter.getSummary()        
        
    def __setTaskManagerSettingsWithUpdate(self,updateDict):
        self.theSettings.updateWith(updateDict)
        self.taskManager.setSettingsTo(self.theSettings)

    def __writeTemplateToFileWithName(self,fileName):
        self._writeContentToFileWithName(STR_INPUT,fileName)
    
GOLD_SETTINGS = {'filesToLoadFrom':['baptism.csv'],
                 'filesToSaveTo':'summary.tex',
                 'roleOfMain':'father'}