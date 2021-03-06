from source.whenUsingTaskManager import whenUsingTaskManager
from source.test_whenUsingEnglishWriterMaker import FATHER_OUTPUT,MOTHER_OUTPUT,CHILD_LISTINGS,OTHER_CHILD_LISTING,COMBINED_CHILDREN_LISTING,TEST_OUTPUT

class whenUsingFileParser(whenUsingTaskManager):    
    def test_whenWritingSectionForFatherGivenAll(self):
        """Tests whether given the minimal input for both father and mother
        of the baptism record in a string representation of the summary writer 
        input to a Mockfile the expected output is returned."""
        self.__test_whenWritingSectionForParentGivenAll('(Fr0)',FATHER_OUTPUT)
    
    def test_whenWritingSectionForMotherGivenAll(self):
        """Tests whether given the minimal input for both father and mother
        of the baptism record in a string representation of the summary writer 
        input to a Mockfile the expected output is returned."""
        self.__test_whenWritingSectionForParentGivenAll('x1(Fr0)',MOTHER_OUTPUT)
        
    def test_whenWritingSectionForFatherGivenOtherChild(self):
        """Tests the same as `test_whenWritingSectionForFatherGivenAll` for a
        different baptism record of the same couple."""
        desiredFileContent = self._testInput.forHermannus()
        self._writeContentToDefaultFile(desiredFileContent)
        actual = self._setupAndRunTaskManagerThenGetOutputAsText('(Fr0)')
        self._assertActualEqualsExpected(actual,FATHER_OUTPUT+OTHER_CHILD_LISTING) 
        
    def test_whenWritingSectionForFatherOfBothChildren(self):
        """Tests whether given baptism input for two children, we can write a 
        single summary section that includes them both."""
        desiredFileContent = self._testInput.forChildren()
        self._writeContentToDefaultFile(desiredFileContent)
        actual = self._setupAndRunTaskManagerThenGetOutputAsText('(Fr0)')
        self._assertActualEqualsExpected(actual,COMBINED_CHILDREN_LISTING)         
        
    def test_whenWritingSecondSection(self):
        """This test asserts that the second section can be written, sub tests will be split of
        and this test will remain as acceptance test."""
        self._writeContentToDefaultFile(TEST_INPUT)
        actual = self._setupAndRunTaskManagerThenGetOutputAsText('(Fr1)')
        self._assertActualEqualsExpected(actual,TEST_OUTPUT['(Fr1)']) 
        
    def test_whenWritingThirdSection(self):
        """This test asserts that the third section can be written, sub tests will be split of
        and this test will remain as acceptance test. This test will show that we can choose the
        infant in a record as our person of focus.
         * the test-input includes records of spanning multiple generations, ensure that the
           children listing does not include possible grandchildren."""
        self._writeContentToDefaultFile(TEST_INPUT)
        actual = self._setupAndRunTaskManagerThenGetOutputAsText('(Fr1.1)')
        self._assertActualEqualsExpected(actual,TEST_OUTPUT['(Fr1.1)'])         
    
    def test_whenWritingFourthSection(self):
        """This test asserts that a (simplified version) of the fourth section can be written, 
        sub tests will be split of and this test will remain as acceptance test. This test will
        show that we can also have a grandchild as summary."""
        self._writeContentToDefaultFile(TEST_INPUT)
        actual = self._setupAndRunTaskManagerThenGetOutputAsText('(Fr1.1.2)')
        self._assertActualEqualsExpected(actual,TEST_OUTPUT['(Fr1.1.2)'])            
        
    def __test_whenWritingSectionForParentGivenAll(self,parentPID,parentOutput):
        self.__writeDefaultContentToDefaultFile() 
        self.__assertActualOutputForParentWithParentOutputEqualsDesiredOutput(parentPID, parentOutput)
    
    def __writeDefaultContentToDefaultFile(self):
        desiredFileContent = self._testInput.forWolterus()
        self._writeContentToDefaultFile(desiredFileContent)
    
    def __assertActualOutputForParentWithParentOutputEqualsDesiredOutput(self,parentPID, parentOutput):
        actualOutput  = self._setupAndRunTaskManagerThenGetOutputAsText(parentPID)
        desiredOutput = parentOutput+CHILD_LISTINGS['default']
        self._assertActualEqualsExpected(actualOutput,desiredOutput)      
        
TEST_INPUT ='father;;;mother;;;infant;;;;;;;;;'+\
            '\nPID;foreNames;lastName;PID;foreNames;lastName;PID;'+\
            'foreNames;gender;denom_0;denom_1;nameOfParish;town;date;;'+\
            '\n;;;;;;;;;;;;;day;month;year'+\
            '\n(Fr1);Jan;Sunder;x1(Fr1);Tela;Mouwe;(Fr1.1);Jan;m;rc;ref;'+\
            'St. Vitus;Freren;13;12;1711'+\
            '\n;Herman;Tijs;;Fenne;Wemerschlage;x1(Fr1.1);'+\
            'Anna Maria;f;ref;;;Freren;8;7;1712'+\
            '\n(Fr1);Jan;Sunder;x1(Fr1);Tela;Mouwe;(Fr1.2);Maria Elisabet;f;ref;;'+\
            ';Freren;8;7;1714'+\
            '\n(Fr1);Jan;Sunder;x1(Fr1);Tela;Mouwe;(Fr1.3);Berend;m;ref;;;Freren;31;5;1717'+\
            '\n(Fr1);Jan;Sunder;x1(Fr1);Tela;Mouwe;(Fr1.4);Berend;m;ref;;;Freren;12;2;1719'+\
            '\n(Fr1.1);Jan;Sunder;x1(Fr1.1);Anna Maria;Tijs;(Fr1.1.1);'+\
            'Thele Marie;f;ref;;;Freren;18;9;1734'+\
            '\n(Fr1.1);Joannis;Sunder;x1(Fr1.1);Anna Maria;Tijes;(Fr1.1.2);'+\
            'Joes Bernardus;m;rc;;St. Vitus;Freren;30;8;1736'+\
            '\n(Fr1.1);;;x1(Fr1.1);;;(Fr1.1.2);Bernardus;m;;ref;;Freren;31;8;1736'+\
            '\n(Fr1.1);;;x1(Fr1.1);;;(Fr1.1.3);Maria;f;rc;ref;St. Vitus;Freren;6;12;1738'+\
            '\n(Fr1.1);;;x1(Fr1.1);;;(Fr1.1.4);Joh. Christoph;m;rc;ref;'+\
            'St. Vitus;Freren;15;1;1741'+\
            '\nVx1(Fr1.1.2);Hermannus;M\"{o}ller;Mx1(Fr1.1.2);Anna Adelheidis;Tieken;'+\
            'x1(Fr1.1.2);Helena;f;rc;;St. Jodocus;B\"{o}rger;24;2;1741'+\
            '\n(Fr1.1);;;x1(Fr1.1);;;(Fr1.1.5);Joannis;m;rc;ref;'+\
            'St. Vitus;Freren;8;9;1743'+\
            '\n(Fr1.1);;;x1(Fr1.1);;;(Fr1.1.6);Henricus;m;rc;ref;'+\
            'St. Vitus;Freren;17;11;1747'+\
            '\n(Fr1.1.2);;;x1(Fr1.1.2);Helena;M\"{o}llers;(Fr1.1.2.1);Anna;;rc;;'+\
            'St. Vitus;Freren;18;12;1762'+\
            '\n(Fr1.1.2);;;x1(Fr1.1.2);;;(Fr1.1.2.2);Thecla Gesina;f;rc;;'+\
            'St. Vitus;Freren;18;12;1762'+\
            '\n(Fr1.1.2);;;x1(Fr1.1.2);;;(Fr1.1.2.3);Joannes Hermannus;;rc;;'+\
            'St. Vitus;Freren;25;5;1765'+\
            '\n(Fr1.1.2);;;x1(Fr1.1.2);;;(Fr1.1.2.4);Joannes Bernardus;;rc;;'+\
            'St. Vitus;Freren;21;4;1767'+\
            '\n(Fr1.1.2);;;x1(Fr1.1.2);;;(Fr1.1.2.5);Hermannus Henericus;;rc;;'+\
            'St. Vitus;Freren;16;9;1769'          

    
    
    