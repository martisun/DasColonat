from source.extended_testcase import ExtendedTestCase

from source.summary_writer import SummaryWriter

from source.mock_file import MockFolderAdapter

SUMMARY_STRUCTURE ="""
{sectionHeader}

{childrenListingIntro}
{childrenDescriptionsInListing}
"""   
    
class MockPhraseWriter(object):
    def fillOut(self,content):
        return content
    
    def childrenDescriptionsInListing(self,name):
        return """{childrenDescriptionsInListing}"""
    
    def childrenListingIntroForParents(self,main,spouse):
        return """{childrenListingIntro}"""
    
    def sectionHeader(self,main):
        return """{sectionHeader}"""
    
    def replaceSpecialCharacters(self,text):
        return text
    
class whenWritingSummary(ExtendedTestCase):
    def test_summaryWriterUsesProperStructure(self):
        """Tests whether the text written by the summary writer 
        includes consecutively the inputfile content and a child 
        listing."""
        summaryWriter = SummaryWriter()
        summaryWriter.setPeopleTo({'main':{},'spouse':{},'children':[{}]})
        summaryWriter.setPhraseWriterTo(MockPhraseWriter())
        actual = summaryWriter.getSummary()
        self._assertActualEqualsExpected(actual,SUMMARY_STRUCTURE)
        
      