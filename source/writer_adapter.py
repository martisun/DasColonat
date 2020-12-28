import re

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
        summaryWriter = self.__writerMaker.parse(self.__baseTemplate)[0]
        summaryTemplate = summaryWriter.writeTo(WriterData.makeFrom(data))
        return summaryTemplate.getText()


    