import re

from source.person_reference import PersonReference
from source.writer_templates import WriterTemplate

class WriterAdapter(object):
    @staticmethod
    def forTemplatePattern(templatePattern):
        writerAdapter = WriterAdapter()
        writerAdapter.__baseTemplate = WriterTemplate(templatePattern)
        return writerAdapter
    
    def setMakerTo(self,writerMaker):
        self.__writerMaker = writerMaker
        
    def write(self,people):
        processedPeople = self.__makePersonReferencesOf(people)
        summaryWriter = self.__writerMaker.parse(self.__baseTemplate)[0]
        summaryTemplate = summaryWriter.writeTo(processedPeople)
        return summaryTemplate.getText()
    
    def __makePersonReferencesOf(self,people):
        return {role:PersonReference.makeFrom(people[role]) for role in people}


    