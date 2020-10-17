import re

from source.writers import AllWriter,TemplaterWriter,ListingWriter
from source.writer_templates import AllWriterTemplate,KeyWriterTemplate,SelectorWriterTemplate,WriterTemplate
from source.language_template import LanguageTemplateSelector
from source.pattern_parsers import PatternParser,TemplaterPatternParser

class WriterMaker(object):
    @staticmethod
    def inLanguage(languageTag):
        templateCollection = LanguageTemplateSelector.getTemplateCollectionInLanguage(languageTag)  
        writerMaker = WriterMaker(templateCollection)
        return writerMaker
    
    def __init__(self,templateCollection):
        self.__templateCollection = templateCollection
    
    def getTemplateWithNameAndInput(self,name,candidatePeople):
        templateGroup     = self.__templateCollection.getTemplateCollectionWithName(name)
        while len(templateGroup) > 0:
            templateDict = self.__templateCollection.initialize(templateGroup.pop(0))
            templateCandidate = self.__initializeTemplateFromInput(templateDict,candidatePeople)
            if templateCandidate.isComplete(): break
        return templateCandidate
    
    def setTemplateCollectionTo(self,templateCollection):
        self.__templateCollection = templateCollection
    
    def parse(self,templateText):
        specifications = re.findall('(\$(\w+)\(([\,\w]+)\))',templateText)
        return [self.__initTemplaterWriterFrom(specification)\
                for specification in specifications]  
    
    @staticmethod
    def __initializeTemplateFromInput(templateDict,candidatePeople):
        if not 'required' in templateDict:
            templateCandidate = AllWriterTemplate()
        elif not 'template' in templateDict:
            if not 'modifier' in templateDict:
                templateCandidate = KeyWriterTemplate()
            else:
                templateCandidate = SelectorWriterTemplate()
        else:
            templateCandidate = WriterTemplate()
        templateCandidate.setupWith(templateDict,candidatePeople)
        return templateCandidate
    
    def __initTemplaterWriterFrom(self,specification):
        blank,name,arguments = specification
        arguments = arguments.split(',')
        if len(arguments) == 1 and 'all' in arguments:
            templaterWriter = AllWriter(blank,name)
            templaterWriter.setPatternParserTo(PatternParser())
        elif name == 'childrenListing':
            templaterWriter = ListingWriter()
        else:
            templaterWriter = TemplaterWriter(blank,name,arguments)
            templaterWriter.setPatternParserTo(TemplaterPatternParser())
        templaterWriter.setMakerTo(self)
        return templaterWriter 