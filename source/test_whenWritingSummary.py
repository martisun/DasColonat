from source.extended_testcase import ExtendedTestCase

from source.summary_writer import SummaryWriter

from source.mock_file import MockFolderAdapter

SUMMARY_STRUCTURE ={'default':"""
{sectionHeader}

{childListingIntro}
{childrenDescriptionsInListing}
""",'multiple children':"""
{sectionHeader}

{childrenListingIntro}
{childrenDescriptionsInListing}
""",
   'no children':"""
{sectionHeader}

{mainDescription}
"""}   
    
class MockPhraseWriter(object):
    def fillOut(self,content):
        return content
    
    def childrenDescriptionsInListing(self,children):
        return """{childrenDescriptionsInListing}"""
    
    def childListingIntroForParents(self,main,spouse):
        return """{childListingIntro}"""
    
    def childrenListingIntroForParents(self,main,spouse):
        return """{childrenListingIntro}"""
    
    def mainDescription(self,main,father,mother):
        return """{mainDescription}"""
    
    def sectionHeader(self,main):
        return """{sectionHeader}"""
    
    def replaceSpecialCharacters(self,text):
        return text
    
class whenWritingSummary(ExtendedTestCase):
    def test_whetherHasChildListingIfOneChild(self):
        """Tests whether the text written by the summary writer 
        includes consecutively the inputfile content and a child 
        listing."""
        summaryWriter = SummaryWriter()
        summaryWriter.setPeopleTo({'main':{},'spouse':{},'children':[{}]})
        summaryWriter.setPhraseWriterTo(MockPhraseWriter())
        actual = summaryWriter.getSummary()
        self._assertActualEqualsExpected(actual,SUMMARY_STRUCTURE['default'])
        
    def test_whetherHasChildrenListingIfMultipleChildren(self):
        """Tests whether the text written by the summary writer 
        includes a special child listing intro if in fact there is
        only one child to treat."""
        summaryWriter = SummaryWriter()
        summaryWriter.setPeopleTo({'main':{},'spouse':{},'children':[{},{}]})
        summaryWriter.setPhraseWriterTo(MockPhraseWriter())
        actual = summaryWriter.getSummary()
        self._assertActualEqualsExpected(actual,SUMMARY_STRUCTURE['multiple children']) 
        
    def test_whetherHasMainDescriptionIfNonTrivialData(self):
        """Tests whether the text written by the summary writer 
        includes a description of the main person, if there is 
        information about his or her life-events."""
        summaryWriter = SummaryWriter()
        summaryWriter.setPeopleTo({'main':{},'father':{},'mother':{}})
        summaryWriter.setPhraseWriterTo(MockPhraseWriter())
        actual = summaryWriter.getSummary()
        self._assertActualEqualsExpected(actual,SUMMARY_STRUCTURE['no children'])         
        
      