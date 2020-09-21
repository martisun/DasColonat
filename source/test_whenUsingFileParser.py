from source.test_whenUsingMockFile import whenUsingMockFile
from source.test_whenUsingEnglishPhraseWriter import FATHER_OUTPUT,MOTHER_OUTPUT,CHILD_LISTINGS,OTHER_CHILD_LISTING,COMBINED_CHILDREN_LISTING

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
        self._writeContentToFileWithName(STR_HEADER+STR_WOLTERUS,
                                         GOLD_SETTINGS['filesToLoadFrom'][0])
        actual = self.__setupAndRunTaskManagerThenGetOutputAsText('father')
        self._assertActualEqualsExpected(actual,FATHER_OUTPUT+CHILD_LISTINGS['default'])  
        
    def test_whenWritingSectionForMotherGivenAll(self):
        """Tests whether given the minimal input for both father and mother
        of the baptism record in a string representation of the summary writer 
        input to a Mockfile the expected output is returned."""
        self._writeContentToFileWithName(STR_HEADER+STR_WOLTERUS,
                                         GOLD_SETTINGS['filesToLoadFrom'][0])
        actual = self.__setupAndRunTaskManagerThenGetOutputAsText('mother')
        self._assertActualEqualsExpected(actual,MOTHER_OUTPUT+CHILD_LISTINGS['default'])
        
    def test_whenWritingSectionForFatherGivenOtherChild(self):
        """Tests the same as `test_whenWritingSectionForFatherGivenAll` for a
        different baptism record of the same couple."""
        self._writeContentToFileWithName(STR_HEADER+STR_HERMANNUS,
                                         GOLD_SETTINGS['filesToLoadFrom'][0])
        actual = self.__setupAndRunTaskManagerThenGetOutputAsText('father')
        self._assertActualEqualsExpected(actual,FATHER_OUTPUT+OTHER_CHILD_LISTING) 
        
    def test_whenWritingSectionForFatherOfBothChildren(self):
        """Tests whether given baptism input for two children, we can write a 
        single summary section that includes them both."""
        self._writeContentToFileWithName(STR_HEADER+STR_WOLTERUS+STR_HERMANNUS,
                                         GOLD_SETTINGS['filesToLoadFrom'][0])
        actual = self.__setupAndRunTaskManagerThenGetOutputAsText('father')
        self._assertActualEqualsExpected(actual,COMBINED_CHILDREN_LISTING) 
        
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
    
STR_HEADER = 'father;;;mother;;child;;;;;;\n'+\
             'PID;firstName;lastName;PID;firstName;PID;'+\
             'firstName;day;month;year;denom_0;nameOfParish' 
        
STR_WOLTERUS  = '\n(Fr0);Jois;Sunder;x1(Fr0);Alheid;(Fr0.1);Wolterus;18;12;1661;rc;St. Vitus' 
STR_HERMANNUS = '\n(Fr0);Jois;Sunder;x1(Fr0);Alheid;(Fr0.2);Hermännus;1;6;1666;rc;St. Vitus'       
        
        