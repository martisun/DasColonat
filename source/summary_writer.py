from source.person_reference import PersonReference

class SummaryWriter(object):    
    def setPhraseWriterTo(self,phraseWriter):
        self.__phraseWriter = phraseWriter
        
    def setPeopleTo(self,people):
        mainParent = PersonReference.fromDict(people['mainParent'])
        self.__phraseWriter.setMainParentTo(mainParent) 
        otherParent = PersonReference.fromDict(people['otherParent'])
        self.__phraseWriter.setOtherParentTo(otherParent) 
        
    def getSummary(self):
        sectionHeader     = self.__compileSectionHeader()
        childListingIntro = self.__phraseWriter.childListingIntro()
        addChildListing   = self.__compileAddChildListing()
        summary =  sectionHeader+childListingIntro+addChildListing
        return summary
    
    def __compileAddChildListing(self):
        addChildListing   = self.__phraseWriter.addChildListing()
        return '\n%s\n'%addChildListing
    
    def __compileSectionHeader(self):
        sectionHeader     = self.__phraseWriter.sectionHeader()
        return '\n%s\n\n'%sectionHeader