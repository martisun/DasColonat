from source.person_reference import PersonReference

class SummaryWriter(object):    
    def setPhraseWriterTo(self,phraseWriter):
        self.__phraseWriter = phraseWriter
        
    def setPeopleTo(self,people):
        self.__main   = PersonReference.fromDict(people['main'])
        self.__spouse = PersonReference.fromDict(people['spouse'])
        
    def getSummary(self):
        sectionHeader     = self.__compileSectionHeader()
        childListingIntro = self.__compileChildListingIntro()
        addChildListing   = self.__compileAddChildListing()
        summary =  sectionHeader+childListingIntro+addChildListing
        return summary
    
    def __compileAddChildListing(self):
        addChildListing   = self.__phraseWriter.addChildListing()
        return '\n%s\n'%addChildListing
    
    def __compileChildListingIntro(self):
        return self.__phraseWriter.childListingIntroForParents(self.__main,self.__spouse)
    
    def __compileSectionHeader(self):
        sectionHeader     = self.__phraseWriter.sectionHeader(self.__main)
        return '\n%s\n\n'%sectionHeader