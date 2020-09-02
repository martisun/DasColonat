from source.person_reference import PersonReference

class SummaryWriter(object):    
    def setPhraseWriterTo(self,phraseWriter):
        self.__phraseWriter = phraseWriter
        
    def setPeopleTo(self,people):
        for role in people:
            nameOfAttribute = self.__getNameOfAttributeForRole(role)
            personReference = PersonReference.fromDict(people[role])
            setattr(self,nameOfAttribute,personReference)
        
    def getSummary(self):
        sectionHeader     = self.__compileSectionHeader()
        childListingIntro = self.__compileChildListingIntro()
        addChildListing   = self.__compileAddChildListing()
        summary =  sectionHeader+childListingIntro+addChildListing
        return self.__phraseWriter.replaceSpecialCharacters(summary)
    
    def __compileAddChildListing(self):
        addChildListing   = self.__phraseWriter.addChildListing(self.__child)
        return '\n%s\n'%addChildListing
    
    def __compileChildListingIntro(self):
        return self.__phraseWriter.childListingIntroForParents(self.__main,self.__spouse)
    
    def __compileSectionHeader(self):
        sectionHeader     = self.__phraseWriter.sectionHeader(self.__main)
        return '\n%s\n\n'%sectionHeader
    
    def __getNameOfAttributeForRole(self,role):
        className       = type(self).__name__
        nameOfAttribute = '_%s__%s'%(className,role)
        return nameOfAttribute