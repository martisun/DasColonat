import re

from source.writer_templates import WriterTemplate
from source.latex_templater import LatexTemplater

from source.record_data import WriterDataDict

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
        template = self.__queue.setupTemplateCandidateFor(writerData)
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
        if writerDataSelection.isEmpty() and not self.__isMainDataSelectable(writerData):
            mainWriterData = writerData.getMainData()
            return self.writeTo(mainWriterData)
        else:
            return super().writeTo(writerDataSelection)
        
    def __isMainDataSelectable(self,writerData):
        return writerData.isMainNonTrivial() and not ('main' in self.__inputRoles)
    
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
        writerData = superTemplate.getWriterData()
        if self.__argument in writerData:
            blankReplacement = self.writeTo(writerData).getText()
        else:
            blankReplacement = ''
        superTemplate.replaceText(self.__blank,blankReplacement)
    
    def writeTo(self,writerData):
        writerDataElements = writerData.selectTag(self.__argument)
        listingText = self.subWriterInListing(writerDataElements)
        return WriterTemplate(listingText)
    
    def subWriterInListing(self,writerData):
        listingTemplates = [self.__compileListingElementOf(writerDataElement)\
                            for writerDataElement in writerData]
        return '\n%s'%WriterTemplate.makeListingOf(listingTemplates)

    def __compileListingElementOf(self,writerData):
        subWriter     = self.__setupSubWriterForData(writerData)
        subWriterData = writerData.getMainData()
        subWriterTemplate = subWriter.writeTo(subWriterData)        
        return subWriterTemplate
    
    def __setupSubWriterForData(self,writerData):
        template = self.__queue.setupTemplateCandidateFor(writerData)
        subWriterList = self.__writerMaker.parse(template)
        return subWriterList[0]     
        
class SubWriterReplacer(object):  
    def __init__(self,parentWriter):
        self.__parent = parentWriter    
    
    def doReplacementsTo(self,template):
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
        for specification in specifications:
            self.__doSingleReplacementInTemplate(specification,template)
            
    def __doSingleReplacementInTemplate(self,specification,template):
        blank,method,arguments = specification
        writerData  = template.getWriterData()
        blankReplacement = self.__determineBlankReplacement(method,arguments,writerData) 
        template.replaceText(blank,blankReplacement)  
    
    def __determineBlankReplacement(self,method,arguments,writerData):
        inputValues = self.__determineTemplaterInputValues(arguments,writerData)      
        return self._templater.evaluate(method,inputValues)
    
    def __determineTemplaterInputValues(self,arguments,writerData):
        if self.__areParametersIn(arguments): return [arguments]
        else: return self.__getParameterValueOfWriterData(arguments,writerData)
        
    def __getParameterValueOfWriterData(self,arguments,writerData):
        parameters = self.extractParameterNamesFromArguments(arguments)
        mainData = writerData.getMainData()
        return mainData.get(parameters)   
    
    def __areParametersIn(self,arguments):
        parameters = self.extractParameterNamesFromArguments(arguments)
        return arguments != '' and len(parameters) == 0
    
    @staticmethod
    def extractParameterNamesFromArguments(arguments):
        return re.findall('\+(\w+)',arguments)   
    
    def _extractSpecificationsFromTemplate(self,template):
        return super()._extractSpecificationsFromTemplate(template,'([\+\w+\,\s\.]+)?')      

class BlankTemplaterCallReplacer(TemplaterCallReplacer):    
    def __init__(self,parentWriter):
        super().__init__()
        self.__parentWriter = parentWriter
    
    def doReplacementsTo(self,template):
        specifications   = self._extractSpecificationsFromTemplate(template)
        if specifications: self.__doNonTrivialReplacement(template,specifications)
        else: self.__doTrivialReplacement(template)
                  
    def __doNonTrivialReplacement(self,template,specifications):
        argument = self.__determineArgumentFromTemplate(template)
        self.__replaceSpecificationsInTemplate(template,specifications,argument)
    
    def __doTrivialReplacement(self,template):
        argument = self.__determineArgumentFromTemplate(template)
        template.replaceBlankBy(argument.getText())        
    
    def __determineArgumentFromTemplate(self,template):
        writerData = template.getWriterData()
        return self.__parentWriter.writeTo(writerData)
    
    def __replaceSpecificationsInTemplate(self,template,specifications,argument):
        blank,method = specifications.pop()
        argument     = self._templater.evaluate(method,[argument.getText()])
        template.replaceText(blank,argument)
    
    def _extractSpecificationsFromTemplate(self,template):
        blankArgument = re.escape(template.blankArgument)
        return super()._extractSpecificationsFromTemplate(template,blankArgument)  
    
        