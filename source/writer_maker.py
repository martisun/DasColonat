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
    
    def parse(self,template):
        return [self.__initTemplaterWriterFrom(specification)\
                for specification in template.getSubWriterSpecifications()]
    
    def __initTemplaterWriterFrom(self,specification):
        blank,name,arguments = specification
        arguments = arguments.replace('+','')
        arguments = arguments.split(',')
        queue     = self.__getTemplateQueueWithName(name)
        if len(arguments) == 1 and 'all' in arguments:
            templaterWriter = AllWriter(blank,queue)
        elif name == 'childrenListing':
            templaterWriter = ListingWriter(blank,queue,arguments)
        else:
            templaterWriter = TemplaterWriter(blank,queue,arguments)
        templaterWriter.setMakerTo(self)
        return templaterWriter 
    
    def __getTemplateQueueWithName(self,name):
        return self.__templateCollection.setupTemplateQueueWithName(name)