from source.extended_testcase import ExtendedTestCase

from source.summary_writer import SummaryWriter

from source.mock_file import MockFolderAdapter

SUMMARY_STRUCTURE ="""
{sectionHeader}

{childListingIntro}
{childListing}
"""   
    
class MockPhraseWriter(object):
    def fillOut(self,content):
        return content
    
    def addChildListing(self):
        return """{childListing}"""
    
    def childListingIntroForParents(self,main,spouse):
        return """{childListingIntro}"""
    
    def sectionHeader(self,main):
        return """{sectionHeader}"""
    
class whenWritingSummary(ExtendedTestCase):
    def test_summaryWriterUsesProperStructure(self):
        """Tests whether the text written by the summary writer 
        includes consecutively the inputfile content and a child 
        listing."""
        summaryWriter = SummaryWriter()
        summaryWriter.setPeopleTo({'main':{},'spouse':{}})
        summaryWriter.setPhraseWriterTo(MockPhraseWriter())
        actual = summaryWriter.getSummary()
        self._assertActualEqualsExpected(actual,SUMMARY_STRUCTURE)
        
      