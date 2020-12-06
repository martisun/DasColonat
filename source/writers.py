import re

from source.writer_templates import WriterTemplate
from source.latex_templater import LatexTemplater
from source.record_data import WriterData

class Writer(object):
    def __init__(self,blank,queue):
        self._blank         = blank
        self._replacers     = []
        self.__queue        = queue
    
    def parseTemplate(self,template):
        return self.__maker.parse(template)
    
    def setMakerTo(self,maker):
        self.__maker = maker
        
    def writeTo(self,writerData):
        print('l.20 writers.py refactoring')
        template = self.__queue.setupTemplateCandidateFor(writerData.toDict())
        for replacer in self._replacers:
            replacer.doReplacementsTo(template)
        template.doAllReplacements()    
        return template
            
class AllWriter(Writer):
    def __init__(self,blank,queue):
        super().__init__(blank,queue)
        self._replacers = [SubWriterReplacer(self)]    
        
class SelectiveWriter(AllWriter):      
    def __init__(self,blank,queue,arguments):
        super().__init__(blank,queue)
        self.__inputRoles = arguments
    
    def writeTo(self,writerData):
        writerDataSelection = writerData.selectTags(self.__inputRoles) 
        if writerDataSelection.isEmpty(): 
            mainWriterData = writerData.getMainData()
            return self.writeTo(mainWriterData)    
        else:
            return super().writeTo(writerDataSelection)       
    
class TemplaterWriter(SelectiveWriter):    
    def __init__(self,*specification):
        super().__init__(*specification)
        self._replacers.insert(0,SimpleTemplaterCallReplacer())
        self.__blankReplacer = BlankTemplaterCallReplacer(self)
        
    def writeIntoTemplateWith(self,superTemplate):
        superTemplate.replaceByBlank(self._blank)
        self.__blankReplacer.doReplacementsTo(superTemplate)

class ListingWriter(object):    
    def __init__(self,blank,queue,arguments):
        self.__blank     = blank
        self.__queue     = queue
        self.__argument = arguments[0]
    
    def setMakerTo(self,writerMaker):
        self.__writerMaker = writerMaker
    
    def writeIntoTemplateWith(self,superTemplate):
        people = superTemplate.getData()
        if self.__argument in people:
            blankReplacement  = self.subWriterInListing(people[self.__argument])
            blankReplacement  = '\n%s'%blankReplacement 
        else:
            blankReplacement = ''
        superTemplate.replaceText(self.__blank,blankReplacement)
    
    def subWriterInListing(self,people):
        listingTemplates = [self.__compileListingElementOf(person) for person in people]
        return WriterTemplate.makeListingOf(listingTemplates)

    def __compileListingElementOf(self,person):
        template = self.__queue.setupTemplateCandidateFor(person)
        subWriter = self.__writerMaker.parse(template)[0]
        print('l.84 writers.py refactoring')
        writerData = WriterData({'main':person})
        subWriterTemplate = subWriter.writeTo(writerData)        
        return subWriterTemplate
        
class SubWriterReplacer(object):  
    def __init__(self,parentWriter):
        self.__parent = parentWriter    
    
    def doReplacementsTo(self,template):
        people = template.getData()
        for subWriter in self.__parent.parseTemplate(template):
            subWriter.writeIntoTemplateWith(template)

class TemplaterCallReplacer(object):
    def __init__(self):
        self._templater = LatexTemplater()
        
    def _extractSpecificationsFromTemplate(self,template,argumentPattern):
        arguments = template.getText()
        return re.findall('(t\.(\w+)\(%s\))'%argumentPattern,arguments)          
    
class SimpleTemplaterCallReplacer(TemplaterCallReplacer):    
    def doReplacementsTo(self,template):
        specifications = self._extractSpecificationsFromTemplate(template)
        for blank,method,arguments in specifications:
            blankReplacement = self.__determineBlankReplacement(method,arguments,template) 
            template.replaceText(blank,blankReplacement)  
    
    def __determineBlankReplacement(self,method,arguments,template):
        people      = template.getData()
        inputValues = self.__determineTemplaterMethod(arguments,people)
        return self._templater.evaluate(method,inputValues)
    
    def __determineTemplaterMethod(self,arguments,people):
        parameters = self.extractParameterNamesFromArguments(arguments)
        if not (len(arguments) > 0 and len(parameters) == 0):
            return people['main'].get(parameters)    
        else: return [arguments]
    
    def _extractSpecificationsFromTemplate(self,template):
        return super()._extractSpecificationsFromTemplate(template,'([\+\w+\,\s\.]+)?')   
    
    @staticmethod
    def extractParameterNamesFromArguments(arguments):
        return re.findall('\+(\w+)',arguments)      

class BlankTemplaterCallReplacer(TemplaterCallReplacer):    
    def __init__(self,parentWriter):
        super().__init__()
        self.__parentWriter = parentWriter
    
    def doReplacementsTo(self,template):
        specifications   = self._extractSpecificationsFromTemplate(template)
        writerData = WriterData(template.getData())
        argumentTemplate = self.__parentWriter.writeTo(writerData)
        argument = argumentTemplate.getText()
        if specifications: 
            self.__replaceSpecificationsInTemplate(template,specifications,argument)
        else: 
            template.replaceBlankBy(argument)       
    
    def __replaceSpecificationsInTemplate(self,template,specifications,argument):
        blank,method = specifications.pop()
        argument     = self._templater.evaluate(method,[argument])
        template.replaceText(blank,argument)
    
    def _extractSpecificationsFromTemplate(self,template):
        blankArgument = re.escape(template.blankArgument)
        return super()._extractSpecificationsFromTemplate(template,blankArgument)  
    
        