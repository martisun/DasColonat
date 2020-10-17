from source.latex_templater import LatexTemplater

class AllWriter(object):
    def __init__(self,blank,name):
        self._blank         = blank
        self.__name         = name
    
    def setMakerTo(self,maker):
        self.__maker = maker
    
    def setPatternParserTo(self,parser):
        self._patternParser = parser
        
    def write(self,people):
        template = self.__maker.getTemplateWithNameAndInput(self.__name,people)
        self._doReplacementsInTemplateTextWith(template) 
        return LatexTemplater.replaceSpecialCharacters(template.getText())
    
    def _writeIntoTemplateWith(self,superTemplate):
        blankReplacement  = self.write(superTemplate.getPeople()) 
        superTemplate.replace(self._blank,blankReplacement)
    
    def _doReplacementsInTemplateTextWith(self,template):
        self.__replaceSubWriterTemplates(template)
        specifications = self._patternParser.extractParametersFromArguments(template.getText())
        for blank,parameter in specifications:
            people = template.getPeople()
            template.replace(blank,people['main'].get(parameter))
        
    def __replaceSubWriterTemplates(self,template):
        for subWriter in self.__maker.parse(template.getText()):
            subWriter._writeIntoTemplateWith(template)    
    
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
        
    def _doReplacementsInTemplateTextWith(self,template):
        self.__replaceTemplaterCalls(template) 
        super()._doReplacementsInTemplateTextWith(template)
        
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
    
    def _writeIntoTemplateWith(self,superTemplate):
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