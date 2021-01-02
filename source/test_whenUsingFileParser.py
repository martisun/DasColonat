from source.test_whenUsingMockFile import whenUsingMockFile
from source.test_whenUsingEnglishWriterMaker import FATHER_OUTPUT,MOTHER_OUTPUT,CHILD_LISTINGS,OTHER_CHILD_LISTING,COMBINED_CHILDREN_LISTING,TEST_OUTPUT

from source.task_manager import TaskManager
from source.settings import Settings
from source.mock_gui import MockGUI
from source.mock_file import MockFolderAdapter

from source.default_settings import getDefaultTestSettings,getPrimalTestHeader

class whenUsingFileParser(whenUsingMockFile):
    def setUp(self):
        self.folderAdapter = MockFolderAdapter()
        defaultTestSettings = getDefaultTestSettings()
        self.defaultTestFileToLoadFrom = defaultTestSettings['filesToLoadFrom'][0]
    
    def test_whenWritingSectionForFatherGivenAll(self):
        """Tests whether given the minimal input for both father and mother
        of the baptism record in a string representation of the summary writer 
        input to a Mockfile the expected output is returned."""
        self.__test_whenWritingSectionForParentGivenAll('father',FATHER_OUTPUT)
    
    def test_whenWritingSectionForMotherGivenAll(self):
        """Tests whether given the minimal input for both father and mother
        of the baptism record in a string representation of the summary writer 
        input to a Mockfile the expected output is returned."""
        self.__test_whenWritingSectionForParentGivenAll('mother',MOTHER_OUTPUT)
        
    def test_whenWritingSectionForFatherGivenOtherChild(self):
        """Tests the same as `test_whenWritingSectionForFatherGivenAll` for a
        different baptism record of the same couple."""
        desiredFileContent = getPrimalTestHeader()+STR_HERMANNUS
        self.__writeContentToDefaultFile(desiredFileContent)
        actual = self.__setupAndRunTaskManagerThenGetOutputAsText('father')
        self._assertActualEqualsExpected(actual,FATHER_OUTPUT+OTHER_CHILD_LISTING) 
        
    def test_whenWritingSectionForFatherOfBothChildren(self):
        """Tests whether given baptism input for two children, we can write a 
        single summary section that includes them both."""
        desiredFileContent = getPrimalTestHeader()+STR_WOLTERUS+STR_HERMANNUS
        self.__writeContentToDefaultFile(desiredFileContent)
        actual = self.__setupAndRunTaskManagerThenGetOutputAsText('father')
        self._assertActualEqualsExpected(actual,COMBINED_CHILDREN_LISTING) 
        
    def test_whenWritingSecondSection(self):
        """This test asserts that the second section can be written, sub tests will be split of
        and this test will remain as acceptance test."""
        self.__writeContentToDefaultFile(TEST_INPUT)
        actual = self.__setupAndRunTaskManagerThenGetOutputAsText('father')
        self._assertActualEqualsExpected(actual,TEST_OUTPUT['(Fr1)']) 
        
    def test_whenWritingThirdSection(self):
        """This test asserts that the third section can be written, sub tests will be split of
        and this test will remain as acceptance test. This test will show that we can choose the
        infant in a record as our person of focus.
         * the test-input includes records of spanning multiple generations, ensure that the
           children listing does not include possible grandchildren."""
        self.__writeContentToDefaultFile(TEST_INPUT)
        actual = self.__setupAndRunTaskManagerThenGetOutputAsText('infant')
        self._assertActualEqualsExpected(actual,TEST_OUTPUT['(Fr1.1)'])         
    
    def __test_whenWritingSectionForParentGivenAll(self,parent,parentOutput):
        self.__writeDefaultContentToDefaultFile() 
        self.__assertActualOutputForParentWithParentOutputEqualsDesiredOutput(parent,parentOutput)
    
    def __writeDefaultContentToDefaultFile(self):
        desiredFileContent = getPrimalTestHeader()+STR_WOLTERUS
        self.__writeContentToDefaultFile(desiredFileContent)
    
    def __writeContentToDefaultFile(self,desiredFileContent):
        desiredFileName    = self.defaultTestFileToLoadFrom
        self._writeContentToFileWithName(desiredFileContent,desiredFileName)
    
    def __assertActualOutputForParentWithParentOutputEqualsDesiredOutput(self,parent,parentOutput):
        actualOutput  = self.__setupAndRunTaskManagerThenGetOutputAsText(parent)
        desiredOutput = parentOutput+CHILD_LISTINGS['default']
        self._assertActualEqualsExpected(actualOutput,desiredOutput) 
    
    def __setupAndRunTaskManagerThenGetOutputAsText(self,roleOfMain):
        settings    = self.__setupGoldSettingsWithRoleOfMain(roleOfMain)
        taskManager = self.__setupTaskManagerWithSettings(settings) 
        taskManager.run()
        return self.__readContentFromDefaultFile()
    
    def __setupGoldSettingsWithRoleOfMain(self,roleOfMain):
        defaultTestSettings = getDefaultTestSettings()
        settings = Settings.setTo(defaultTestSettings)
        settings.updateWith({'roleOfMain':roleOfMain})
        return settings
    
    def __setupTaskManagerWithSettings(self,settings):
        taskManager = TaskManager()
        taskManager.setGUITo(MockGUI())
        taskManager.setFolderAdapterTo(self.folderAdapter)
        taskManager.setSettingsTo(settings)
        return taskManager
    
    def __readContentFromDefaultFile(self):
        defaultTestSettings = getDefaultTestSettings()
        fileNameWithSavedData = defaultTestSettings['filesToSaveTo']
        return self._readContentFromFileWithName(fileNameWithSavedData)

        
STR_WOLTERUS  = '\n(Fr0);Jois;Sunder;x1(Fr0);Alheid;(Fr0.1);Wolterus;rc;St. Vitus;18;12;1661' 
STR_HERMANNUS = '\n(Fr0);Jois;Sunder;x1(Fr0);Alheid;(Fr0.2);Hermännus;rc;St. Vitus;1;6;1666'       
        
TEST_INPUT = 'father;;;mother;;;infant;;;;;;;;'+\
             '\nPID;foreNames;lastName;PID;foreNames;lastName;PID;'+\
             'foreNames;gender;denom_0;denom_1;nameOfParish;date;;'+\
             '\n;;;;;;;;;;;;day;month;year'+\
             '\n(Fr1);Jan;Sunder;x1(Fr1);Tela;Mouwe;(Fr1.1);Jan;m;rc;ref;St. Vitus;13;12;1711'+\
             '\n(Fr1);Jan;Sunder;x1(Fr1);Tela;Mouwe;(Fr1.2);Maria Elisabet;f;ref;;;8;7;1714'+\
             '\n(Fr1);Jan;Sunder;x1(Fr1);Tela;Mouwe;(Fr1.3);Berend;m;ref;;;31;5;1717'+\
             '\n(Fr1);Jan;Sunder;x1(Fr1);Tela;Mouwe;(Fr1.4);Berend;m;ref;;;12;2;1719'+\
             '\n(Fr1.1);Jan;Sunder;x1(Fr1.1);Enne;Tijs;(Fr1.1.1);Thele Marie;f;ref;;;18;9;1734'  
                

    
    
    