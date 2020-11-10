import re

from source.writers import AllWriter,TemplaterWriter,ListingWriter
from source.language_template import LanguageTemplateCollections
from source.pattern_parsers import PatternParser,TemplaterPatternParser

class WriterMaker(object):
    @staticmethod
    def inLanguage(languageTag):
        templateCollection = LanguageTemplateCollections.getWithLanguageTag(languageTag)  
        writerMaker = WriterMaker(templateCollection)
        return writerMaker
    
    def __init__(self,templateCollection):
        self.__templateCollection = templateCollection
    
    def setTemplateCollectionTo(self,templateCollection):
        self.__templateCollection = templateCollection
    
    def getTemplateQueueWithName(self,name):
        return self.__templateCollection.setupTemplateQueueWithName(name)
    
    def parse(self,templateText,tmp):
        specifications = re.findall('(\$(\w+)\(([\,\w]+)\))',templateText)
        if len(specifications) > 0:
            return [self.__initTemplaterWriterFrom(specification,tmp)\
                    for specification in specifications]  
        else:
            specifications = re.findall('(\$(\w+)\(\+([\,\w]+)\))',templateText)
            if len(specifications) > 0:
                return [self.__initTemplaterWriterFrom(specifications[0],tmp)]
            else: return []
    
    def __initTemplaterWriterFrom(self,specification,tmp):
        blank,name,arguments = specification
        arguments = arguments.split(',')
        queue     = self.getTemplateQueueWithName(name)
        if len(arguments) == 1 and 'all' in arguments:
            templaterWriter = AllWriter(blank,queue)
        elif name == 'childrenListing':
            templaterWriter = ListingWriter()
        else:
            templaterWriter = TemplaterWriter(blank,queue,arguments)
        templaterWriter.setMakerTo(self)
        return templaterWriter 