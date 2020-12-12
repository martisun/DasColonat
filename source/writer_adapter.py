import re

from source.person_reference import PersonReference
from source.writer_templates import WriterTemplate
from source.record_data import WriterData

from source.writers import TemplaterWriter

class WriterAdapter(object):
    @staticmethod
    def forTemplatePattern(templatePattern):
        writerAdapter = WriterAdapter()
        writerAdapter.__baseTemplate = WriterTemplate(templatePattern)
        return writerAdapter
    
    def setMakerTo(self,writerMaker):
        self.__writerMaker = writerMaker
        
    def write(self,data):
        processedData = self.__makePersonReferencesOf(data)
        summaryWriter = self.__writerMaker.parse(self.__baseTemplate)[0]
        summaryTemplate = summaryWriter.writeTo(WriterData(processedData))
        return summaryTemplate.getText()
    
    def __makePersonReferencesOf(self,data):
        return {role:PersonReference.makeFrom(data[role]) for role in data}


    