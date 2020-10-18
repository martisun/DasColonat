import re

from source.latex_templater import LatexTemplater

class Writer(object):
    def __init__(self,blank,name):
        self._blank         = blank
        self._replacers     = []
        self.__name         = name
    
    def parseTemplate(self,template):
        return self.__maker.parse(template.getText())
    
    def setMakerTo(self,maker):
        self.__maker = maker
        
    def write(self,people):
        template = self.__maker.getTemplateWithNameAndInput(self.__name,people)
        for replacer in self._replacers:
            replacer.doReplacementsTo(template)
        return LatexTemplater.replaceSpecialCharacters(template.getText())   
    
    def writeIntoTemplateWith(self,superTemplate):
        blankReplacement  = self.write(superTemplate.getPeople()) 
        superTemplate.replace(self._blank,blankReplacement)     
        
class SubWriterReplacer(object):  
    def __init__(self,parentWriter):
        self.__parent = parentWriter    
    
    def doReplacementsTo(self,template):
        for subWriter in self.__parent.parseTemplate(template):
            subWriter.writeIntoTemplateWith(template)             

class ParameterReplacer(object):
    def doReplacementsTo(self,template):
        specifications = self.__extractSpecificationsFromTemplate(template)
        for blank,parameter in specifications:
            people = template.getPeople()
            value  = people['main'].get(parameter) 
            template.replace(blank,value)   
            
    @staticmethod
    def __extractSpecificationsFromTemplate(template):
        arguments = template.getText()
        return re.findall('(\(\+(\w+)\))',arguments)
            
class AllWriter(Writer):
    def __init__(self,blank,name):
        super().__init__(blank,name)
        self._replacers = [SubWriterReplacer(self),ParameterReplacer()]
            
class SelectiveWriter(AllWriter):      
    def __init__(self,blank,name,arguments):
        super().__init__(blank,name)
        self.__inputRoles   = arguments
    
    def write(self,people):
        peopleCandidates = self.__getPeopleCandidatesFromInputRoles(people)
        return super().write(peopleCandidates)
    
    def __getPeopleCandidatesFromInputRoles(self,people):
        peopleCandidates = []        
        for inputRole in self.__inputRoles:
            if inputRole in people: peopleCandidates.append(people[inputRole])
            else:                   peopleCandidates
        return peopleCandidates 

class TemplaterWriter(SelectiveWriter):
    def __init__(self,*specification):
        super().__init__(*specification)
        self.__templater     = LatexTemplater()
    
    def setPatternParserTo(self,patternParser):
        self._patternParser = patternParser
    
    def _doReplacementsInTemplateTextWith(self,template):
        self.__replaceTemplaterCalls(template) 
        super().doReplacementsTo(template)
        
    def _writeIntoTemplateWith(self,superTemplate):
        blankedArgument   = self._patternParser.blankedArgument
        blankReplacement  = self.write(superTemplate.getPeople()) 
        superTemplate.replace(self._blank,blankedArgument)
        self.__applyTemplaterWithValueToBlankIn(blankReplacement,superTemplate)
    
    def __applyTemplaterWithValueToBlankIn(self,argument,superTemplate):
        specifications  = self._patternParser.extractBlankedSpecsFrom(superTemplate.getText())
        if specifications: 
            blank,method     = specifications.pop()
            blankReplacement = self.__templater.evaluate(method,[argument])
            superTemplate.replace(blank,blankReplacement)  
        else:  
            superTemplate.replace(self._patternParser.blankedArgument,argument)  
    
    def __determineTemplaterBlankReplacement(self,method,arguments,people):
        parameters = self._patternParser.extractParameterNamesFromArguments(arguments)
        if not (len(arguments) > 0 and len(parameters) == 0):
            values = people['main'].get(parameters)    
            return self.__templater.evaluate(method,values)
        else:
            return self.__templater.evaluate(method,[arguments])
    
    def __replaceTemplaterCalls(self,template):
        specifications = self._patternParser.extractFullSpecsFrom(template.getText())
        for blank,method,arguments in specifications:
            blankReplacement = self.__determineTemplaterBlankReplacement(method,arguments, template.getPeople()) 
            template.replace(blank,blankReplacement)
            
class ListingWriter(object):    
    def __init__(self):
        self.__templater = LatexTemplater()       
    
    def setMakerTo(self,writerMaker):
        self.__writerMaker = writerMaker
    
    def writeIntoTemplateWith(self,superTemplate):
        people = superTemplate.getPeople()
        if 'children' in people:
            blankReplacement  = self.childrenDescriptionsInListing(people['children'])
            blankReplacement  = '\n%s'%blankReplacement 
        else:
            blankReplacement = ''
        superTemplate.replace('$childrenListing(children)',blankReplacement)
    
    def childrenDescriptionsInListing(self,children):
        childrenListing = [self.__compileChildDescriptionInListingOf(child) for child in children]
        return self.__templater.compileListingOf(childrenListing)

    def __compileChildDescriptionInListingOf(self,child):  
        childDescriptionWriter = self.__writerMaker.parse('$childDescription(main)')[0]
        return childDescriptionWriter.write({'main':child})              