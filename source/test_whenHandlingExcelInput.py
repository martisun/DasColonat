import subprocess as sub 
import os

from source.whenUsingTaskManager import whenUsingTaskManager

class whenUsingExcelInput(whenUsingTaskManager):    
    def test_whenConsideringExcelInput(self):
        """Tests whether excel can put out texts that can be handled by the task_manager."""
        generatedFileContent = self.__readExcelGeneratedFileContent()
        desiredFileContent   = self._testInput.forWolterus()
        self._assertActualEqualsExpected(generatedFileContent,desiredFileContent)
        
    def test_whenConsideringLatexOutput(self):
        """Tests whether the desired latex-files can be produced."""
        desiredFileContent = self._testInput.forWolterus()
        self._writeContentToDefaultFile(desiredFileContent)
        actual = self._setupAndRunTaskManagerThenGetOutputAsText('(Fr0)')
        overviewText = """\chapter{The lineage of (Fr0)}
\input{_Fr0_}"""
        with open("./testSummary/description.tex",'w') as fileObject:
            fileObject.write(overviewText)
        with open("./testSummary/_Fr0_.tex",'w') as fileObject:
            actual = actual.replace('\r','\\r')
            fileObject.write(actual)  
        self.__assertPrimalTestSummaryOverviewEquals(overviewText)
        self.__assertPrimalTestSummaryEntryEquals(actual)
        
    def test_integrationExcelPythonLatex(self):
        """Tests whether the desired excel data can be put out to a latex text."""
        generatedFileContent = self.__readExcelGeneratedFileContent()
        self._writeContentToDefaultFile(generatedFileContent)  
        actual = self._setupAndRunTaskManagerThenGetOutputAsText('(Fr0)')
        overviewText = """\chapter{The lineage of (Fr0)}
\input{_Fr0_}"""
        with open("./testSummary/description.tex",'w') as fileObject:
            fileObject.write(overviewText)
        with open("./testSummary/_Fr0_.tex",'w') as fileObject:
            actual = actual.replace('\r','\\r')
            fileObject.write(actual)    
        self.__assertPrimalTestSummaryOverviewEquals(overviewText)
        self.__assertPrimalTestSummaryEntryEquals(actual)
        
    def test_integrationLatexRun(self):
        """Tests whether the produced latex text can be run."""
        generatedFileContent = self.__readExcelGeneratedFileContent()
        self._writeContentToDefaultFile(generatedFileContent)
        self.__writePDFLatexInputWithTaskManagerForPrimalSummaryEntry()    
        self.__runPDFLatexForTestSummary()
        self.assertTrue(os.path.isfile('./testSummary/overview.pdf'))  
    
    def __assertPrimalTestSummaryOverviewEquals(self,overviewText):
        with open("./testSummary/description.tex") as fileObject:
            readOverviewText = fileObject.read()
        self._assertActualEqualsExpected(readOverviewText,overviewText)    
    
    def __assertPrimalTestSummaryEntryEquals(self,actual):    
        with open("./testSummary/_Fr0_.tex") as fileObject:
            readActual = fileObject.read()   
        self._assertActualEqualsExpected(readActual,actual)    
    
    def __writePDFLatexInputWithTaskManagerForPrimalSummaryEntry(self):
        actual = self._setupAndRunTaskManagerThenGetOutputAsText('(Fr0)')
        overviewText = """\chapter{The lineage of (Fr0)}
\input{_Fr0_}"""
        with open("./testSummary/description.tex",'w') as fileObject:
            fileObject.write(overviewText)
        with open("./testSummary/_Fr0_.tex",'w') as fileObject:
            actual = actual.replace('\b','\\b')
            actual = actual.replace('\r','\\r')
            actual = actual.replace('\t','\\t')
            fileObject.write(actual) 
        print('l.149 test_whenUsingFileParser.py refactoring (use existing framework)')
    
    def __readExcelGeneratedFileContent(self):
        with open("./input/test_whenConsideringExcelOutput.csv") as fileObject:
            excelGeneratedFileContent = fileObject.read()
        return excelGeneratedFileContent.replace(',',';') 
    
    def __runPDFLatexForTestSummary(self):
        os.chdir('./testSummary')
        if os.path.isfile('overview.pdf'):
            sub.call(['rm','overview.pdf'])
        sub.call(['pdflatex','overview.tex'])
        sub.call(['pdflatex','overview.tex'])
        os.chdir('../')        