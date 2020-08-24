from source.extended_testcase import ExtendedTestCase

from source.summary_writer import SummaryWriter
from source.phrase_writer import PhraseWriter

class whenUsingSummaryWriter(ExtendedTestCase):
    def setUp(self):
        self.summaryWriter = SummaryWriter()
        self.phraseWriter = PhraseWriter.inLanguage('en')
        self.summaryWriter.setPhraseWriterTo(self.phraseWriter)
    
    def test_whenWritingSectionForFather(self):
        """Tests whether the LatexTemplate writes a proper personal summary
        section for the father in a baptism record given minimal input."""
        self.summaryWriter.setPeopleTo(FATHER_INPUT)
        actual = self.summaryWriter.getSummary()
        self._assertActualEqualsExpected(actual,FATHER_OUTPUT+CHILD_LISTING)
        
    def test_whenWritingSectionForMother(self):
        """Tests whether the LatexTemplate writes a proper personal summary
        section for the mother in a baptism record given minimal input."""
        self.summaryWriter.setPeopleTo(MOTHER_INPUT)
        actual = self.summaryWriter.getSummary()
        self._assertActualEqualsExpected(actual,MOTHER_OUTPUT+CHILD_LISTING)        

FATHER_INPUT = {'mainParent':{'PID':'(Fr0)','firstName':'Jois','lastName':'Sunder','gender':'m'},
                   'otherParent':{'PID':'x1(Fr0)','firstName':'Alheid'}}
FATHER_OUTPUT="""
\section{\pidt{(Fr0)}-- Sunder, Jois --~\Mars}\label{sec:(Fr0)}

From a relationship between Jois \textbf{S}under\pids{(Fr0)} and Alheid\pids{x1(Fr0)} was brought forth:"""  

MOTHER_INPUT = {'mainParent':{'PID':'x1(Fr0)','firstName':'Alheid','gender':'v'},
                   'otherParent':{'PID':'(Fr0)','firstName':'Jois','lastName':'Sunder'}}
MOTHER_OUTPUT="""
\section{\pidt{x1(Fr0)}-- Alheid --~\Venus}\label{sec:x1(Fr0)}

From a relationship between Alheid\pids{x1(Fr0)} and Jois \textbf{S}under\pids{(Fr0)} was brought forth:"""

CHILD_LISTING = """
\begin{itemize}
\item[\emph{\rom{1}.}] Wolterus~(\textbf{?})~\pids{(Fr0.1)} was baptised on the 18\supscr{th} of December 1661 before the catholic church of the {\it St. Vitus} parish at Freren.
\end{itemize}
"""