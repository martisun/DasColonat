from source.extended_testcase import ExtendedTestCase

from source.summary_writer import SummaryWriter
from source.phrase_writer import PhraseWriter

from source.settings import Settings
from source.task_manager import TaskManager
from source.mock_gui import MockGUI
from source.mock_file import MockFolderAdapter
from source.test_whenUsingMockFile import whenUsingMockFile

class whenUsingEnglishPhraseWriter(ExtendedTestCase):
    def setUp(self):
        self.summaryWriter = SummaryWriter()
        self.phraseWriter = PhraseWriter.inLanguage('en')
        self.summaryWriter.setPhraseWriterTo(self.phraseWriter)
    
    def test_whenWritingSectionForFather(self):
        """Tests whether given the input to the minimal input to the summary writer, the
        correct output is returned by the phrase writer in a baptism record."""
        self.summaryWriter.setPeopleTo(FATHER_INPUT)
        actual = self.summaryWriter.getSummary()
        self._assertActualEqualsExpected(actual,FATHER_OUTPUT+CHILD_LISTING)
        
    def test_whenWritingSectionForMother(self):
        """Tests whether given the input to the minimal input to the summary writer, the
        correct output is returned by the phrase writer in a baptism record."""
        self.summaryWriter.setPeopleTo(MOTHER_INPUT)
        actual = self.summaryWriter.getSummary()
        self._assertActualEqualsExpected(actual,MOTHER_OUTPUT+CHILD_LISTING)        

class whenUsingFileLoader(whenUsingMockFile):
    def setUp(self):
        self.folderAdapter = MockFolderAdapter()
    
    def test_whenWritingSectionForFatherGivenMain(self):
        """Tests whether given the minimal input of the baptism record in 
        a string representation of the summary writer input to a MockFile 
        the same output is returned."""
        MOD_FATHER_INPUT = {'main':{'PID':'(Fr0)','firstName':'Jois',
                                    'lastName':'Sunder', 'gender':'m'}}
        STR_MOTHER_INPUT = 'mother;;\nPID;firstName\nx1(Fr0);Alheid'
        self._writeContentToFileWithName((STR_MOTHER_INPUT,MOD_FATHER_INPUT),
                                          GOLD_SETTINGS['filesToLoadFrom'][0])
        actual = self.__setupAndRunTaskManagerThenGetOutputAsText('father')
        self._assertActualEqualsExpected(actual,FATHER_OUTPUT+CHILD_LISTING) 
        
    def test_whenWritingSectionForFatherGivenSpouse(self):
        """Tests whether given the minimal input of the baptism record in 
        a string representation of the summary writer input to a MockFile 
        the same output is returned."""
        MOD_FATHER_INPUT = {'spouse':{'PID':'x1(Fr0)','firstName':'Alheid'}}
        self._writeContentToFileWithName((STR_FATHER_INPUT,MOD_FATHER_INPUT),
                                          GOLD_SETTINGS['filesToLoadFrom'][0])
        actual = self.__setupAndRunTaskManagerThenGetOutputAsText('father')
        self._assertActualEqualsExpected(actual,FATHER_OUTPUT+CHILD_LISTING)         
        
    def test_whenWritingSectionForMotherGivenMain(self):
        """Tests whether given the minimal input of the baptism record in 
        a string representation of the summary writer input to a MockFile 
        the same output is returned."""
        MOD_MOTHER_INPUT = {'main':{'PID':'x1(Fr0)','firstName':'Alheid','gender':'v'}}
        self._writeContentToFileWithName((STR_FATHER_INPUT,MOD_MOTHER_INPUT),
                                          GOLD_SETTINGS['filesToLoadFrom'][0])
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

STR_FATHER_INPUT   = 'father;;\nPID;firstName;lastName\n(Fr0);Jois;Sunder'

FATHER_INPUT = {'main':{'PID':'(Fr0)','firstName':'Jois','lastName':'Sunder','gender':'m'},
                'spouse':{'PID':'x1(Fr0)','firstName':'Alheid'}}

FATHER_OUTPUT="""
\section{\pidt{(Fr0)}-- Sunder, Jois --~\Mars}\label{sec:(Fr0)}

From a relationship between Jois \textbf{S}under\pids{(Fr0)} and Alheid\pids{x1(Fr0)} was brought forth:"""  

MOTHER_INPUT = {'main':{'PID':'x1(Fr0)','firstName':'Alheid','gender':'v'},
                'spouse':{'PID':'(Fr0)','firstName':'Jois','lastName':'Sunder'}}

MOTHER_OUTPUT="""
\section{\pidt{x1(Fr0)}-- Alheid --~\Venus}\label{sec:x1(Fr0)}

From a relationship between Alheid\pids{x1(Fr0)} and Jois \textbf{S}under\pids{(Fr0)} was brought forth:"""

CHILD_LISTING = """
\begin{itemize}
\item[\emph{\rom{1}.}] Wolterus~(\textbf{?})~\pids{(Fr0.1)} was baptised on the 18\supscr{th} of December 1661 before the catholic church of the {\it St. Vitus} parish at Freren.
\end{itemize}
"""
