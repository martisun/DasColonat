import re
from source.person_reference import PersonReference

class WriterAdapter(object):
    @staticmethod
    def forTemplatePattern(templatePattern):
        writerAdapter = WriterAdapter()
        writerAdapter.__templatePattern = templatePattern
        return writerAdapter
    
    def setMakerTo(self,writerMaker):
        self.__writerMaker = writerMaker
        
    def write(self,people):
        processedPeople = self.__makePersonReferencesOf(people)
        summaryWriter = self.__writerMaker.parse(self.__templatePattern,'')[0]
        return summaryWriter.write(processedPeople)
    
    def __makePersonReferencesOf(self,people):
        return {role:PersonReference.makeFrom(people[role]) for role in people}


    