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
        print('summaryWriter l.14: clean code.')
        sectionHeader                 = self.__compileSectionHeader()
        if self.__getNameOfAttributeForRole('father') in self.__dict__:
            mainDescription = self.__phraseWriter.mainDescription(self.__main,\
                                                    self.__father,self.__mother)
        else:
            mainDescription           = ''
        if self.__getNameOfAttributeForRole('children') in self.__dict__:
            childrenListingIntro          = self.__compileChildrenListingIntro()
            childrenDescriptionsInListing = self.__compileChildrenDescriptionsInListing()
            childrenListing = childrenListingIntro+childrenDescriptionsInListing
        else: 
            childrenListing = '\n'
        summary =  sectionHeader+mainDescription+childrenListing
        return self.__phraseWriter.replaceSpecialCharacters(summary)
    
    def __compileChildrenDescriptionsInListing(self):
        addChildListing   = self.__phraseWriter.childrenDescriptionsInListing(self.__children)
        return '\n%s\n'%addChildListing
    
    def __compileChildrenListingIntro(self):
        if len(self.__children) == 1:
            return self.__phraseWriter.childListingIntroForParents(self.__main,self.__spouse)
        else:
            return self.__phraseWriter.childrenListingIntroForParents(self.__main,self.__spouse)
    
    def __compileSectionHeader(self):
        sectionHeader     = self.__phraseWriter.sectionHeader(self.__main)
        return '\n%s\n\n'%sectionHeader
    
    def __getNameOfAttributeForRole(self,role):
        className       = type(self).__name__
        nameOfAttribute = '_%s__%s'%(className,role)
        return nameOfAttribute