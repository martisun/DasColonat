from source.person_reference import PersonReference

class SummaryWriter(object):    
    def setPhraseWriterTo(self,phraseWriter):
        self.__phraseWriter = phraseWriter
        
    def setPeopleTo(self,people):
        for role in people:
            nameOfAttribute  = self.__getNameOfAttributeForRole(role)
            personReferences = PersonReference.makeFrom(people[role])
            setattr(self,nameOfAttribute,personReferences)
        
    def getSummary(self):
        sectionHeader                 = self.__compileSectionHeader()
        childrenListingIntro          = self.__compileChildrenListingIntro()
        childrenDescriptionsInListing = self.__compileChildrenDescriptionsInListing()
        summary =  sectionHeader+childrenListingIntro+childrenDescriptionsInListing
        return self.__phraseWriter.replaceSpecialCharacters(summary)
    
    def __compileChildrenDescriptionsInListing(self):
        addChildListing   = self.__phraseWriter.childrenDescriptionsInListing(self.__children)
        return '\n%s\n'%addChildListing
    
    def __compileChildrenListingIntro(self):
        return self.__phraseWriter.childrenListingIntroForParents(self.__main,self.__spouse)
    
    def __compileSectionHeader(self):
        sectionHeader     = self.__phraseWriter.sectionHeader(self.__main)
        return '\n%s\n\n'%sectionHeader
    
    def __getNameOfAttributeForRole(self,role):
        className       = type(self).__name__
        nameOfAttribute = '_%s__%s'%(className,role)
        return nameOfAttribute