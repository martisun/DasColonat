import re
from source.person_reference import PersonReference

class SummaryWriter(object):    
    def setPhraseWriterTo(self,phraseWriter):
        self.__phraseWriter = phraseWriter
        
    def setPeopleTo(self,people):
        self.__people = {}
        for role in people:
            nameOfAttribute  = self.__getNameOfAttributeForRole(role)
            personReferences = PersonReference.makeFrom(people[role])
            setattr(self,nameOfAttribute,personReferences)
            if role != 'children': self.__people.update({role:personReferences})
        
    def getSummary(self,writerMaker):
        summaryWriter = writerMaker.parse('$summary(all)')[0]
        sectionHeader = summaryWriter.write(self.__people)
        self.__phraseWriter.setWriterMakerTo(writerMaker)
        mainDescription   = self.__compileMainParagraph()
        childrenListing  = self.__compileChildrenListing()         
        summary =  sectionHeader+mainDescription+childrenListing
        return self.__phraseWriter.replaceSpecialCharacters(summary)
    
    def __compileChildrenListing(self):
        if self.__getNameOfAttributeForRole('children') in self.__dict__:
            childrenListingIntro          = self.__compileChildrenListingIntro()
            childrenDescriptionsInListing = self.__compileChildrenDescriptionsInListing()
            return childrenListingIntro+childrenDescriptionsInListing
        else: 
            return '\n'
    
    def __compileChildrenDescriptionsInListing(self):
        addChildListing   = self.__phraseWriter.childrenDescriptionsInListing(self.__children)
        return '\n%s\n'%addChildListing
    
    def __compileChildrenListingIntro(self):
        if len(self.__children) == 1:
            return self.__phraseWriter.childListingIntroForParents(self.__main,self.__spouse)
        else:
            return self.__phraseWriter.childrenListingIntroForParents(self.__main,self.__spouse)
    
    def __compileMainParagraph(self):
        father = self.__getRecordOf('father')
        mother = self.__getRecordOf('mother')
        if self.__main.isMoreThanReference() and (father and mother):
            return self.__phraseWriter.mainDescription(self.__main,father,mother)
        else:
            return ''
    
    def __getRecordOf(self,recordRole):
        attributeNameOfRecordRole = self.__getNameOfAttributeForRole(recordRole)
        if attributeNameOfRecordRole in self.__dict__:
            return getattr(self,attributeNameOfRecordRole)
        else: return {}
    
    def __getNameOfAttributeForRole(self,role):
        className       = type(self).__name__
        nameOfAttribute = '_%s__%s'%(className,role)
        return nameOfAttribute


    