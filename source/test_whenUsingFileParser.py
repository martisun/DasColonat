from source.test_whenUsingMockFile import whenUsingMockFile
from source.test_whenUsingEnglishPhraseWriter import FATHER_OUTPUT,MOTHER_OUTPUT,CHILD_LISTING

from source.task_manager import TaskManager
from source.settings import Settings
from source.mock_gui import MockGUI
from source.mock_file import MockFolderAdapter

class whenUsingFileParser(whenUsingMockFile):
    def setUp(self):
        self.folderAdapter = MockFolderAdapter()
    
    def test_whenWritingSectionForFatherGivenAll(self):
        """Tests whether given the minimal input for both father and mother
        of the baptism record in a string representation of the summary writer 
        input to a Mockfile the expected output is returned."""
        self._writeContentToFileWithName(STR_INPUT,GOLD_SETTINGS['filesToLoadFrom'][0])
        actual = self.__setupAndRunTaskManagerThenGetOutputAsText('father')
        self._assertActualEqualsExpected(actual,FATHER_OUTPUT+CHILD_LISTING)  
        
    def test_whenWritingSectionForMotherGivenAll(self):
        """Tests whether given the minimal input for both father and mother
        of the baptism record in a string representation of the summary writer 
        input to a Mockfile the expected output is returned."""
        self._writeContentToFileWithName(STR_INPUT,GOLD_SETTINGS['filesToLoadFrom'][0])
        actual = self.__setupAndRunTaskManagerThenGetOutputAsText('mother')
        self._assertActualEqualsExpected(actual,MOTHER_OUTPUT+CHILD_LISTING)      
        
    def __setupAndRunTaskManagerThenGetOutputAsText(self,roleOfMain):
        settings = Settings.setTo(GOLD_SETTINGS)
        settings.updateWith({'roleOfMain':roleOfMain})
        theGUI   = MockGUI()
        taskManager = TaskManager()
        taskManager.setGUITo(theGUI)
        taskManager.setFolderAdapterTo(self.folderAdapter)
        taskManager.setSettingsTo(settings)
        taskManager.run()
        actual = self._readContentFromFileWithName(GOLD_SETTINGS['filesToSaveTo'])
        return actual

GOLD_SETTINGS = {'filesToLoadFrom':['baptism.csv'],\
                 'filesToSaveTo':'summary.tex'}    
    
STR_INPUT = 'father;;;mother;;child;;;;\n'+\
            'PID;firstName;lastName;PID;firstName;PID;firstName;day;month;year\n'+\
            '(Fr0);Jois;Sunder;x1(Fr0);Alheid;(Fr0.1);Wolterus;18;12;1661'    