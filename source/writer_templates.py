import re

from source.latex_templater import LatexTemplater
    
class Writer(object):      
    def __init__(self,specification):
        blank,name,arguments = specification
        self._blank         = blank
        self._patternParser = TemplaterPatternParser()
        self.__name          = name
        self.__inputRoles    = arguments.split(',')
    
    def setParserTo(self,parser):
        self.__parser = parser
    
    def write(self,people):
        peopleCandidates = self.__getPeopleCandidatesFromInputRoles(people)
        template = WriterTemplate.findGivenNameAndInput(self.__name,peopleCandidates)
        self._doReplacementsInTemplateTextWith(template)
        return template.getText()    
    
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
        for subWriter in self.__parser.parse(template.getText()):
            subWriter._writeIntoTemplateWith(template) 
    
    def __getPeopleCandidatesFromInputRoles(self,people):
        if 'all' in self.__inputRoles: return people
        else: return self.__selectPeopleCandidatesFromInputRoles(people)
    
    def __selectPeopleCandidatesFromInputRoles(self,people):
        peopleCandidates = []        
        for inputRole in self.__inputRoles:
            if inputRole in people: peopleCandidates.append(people[inputRole])
            else:                   peopleCandidates
        return peopleCandidates
    
class TemplaterWriter(Writer):
    def __init__(self,specification):
        super().__init__(specification)
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
        
class TemplaterPatternParser(object):
    blankedArgument = '+blank'
    
    @staticmethod
    def extractFullSpecsFrom(templateText):
        return re.findall('(t\.(\w+)\(([\+\w+\,]+)?\))',templateText)
    
    @staticmethod
    def extractBlankedSpecsFrom(templateText):
        return re.findall('(t\.(\w+)\(\+blank\))',templateText)
    
    @staticmethod
    def extractParameterNamesFromArguments(arguments):
        return re.findall('\+(\w+)',arguments) 
    
    @staticmethod
    def extractParametersFromArguments(arguments):
        return re.findall('(\(\+(\w+)\))',arguments) 

class WriterParser(object):
    @staticmethod
    def initTemplaterWriterFrom(specification):
        templaterWriter = TemplaterWriter(specification)
        templaterWriter.setParserTo(WriterParser())
        return templaterWriter
    
    @staticmethod
    def parse(templateText):
        specifications = re.findall('(\$(\w+)\(([\,\w]+)\))',templateText)
        return [WriterParser.initTemplaterWriterFrom(specification)\
                for specification in specifications]    
    
class WriterTemplate(object):
    __template = {'summary':[{'required':['all'],'template':"""
$sectionHeader(main)

$mainParagraph(main,father,mother)"""}],    
    'sectionHeader':[{'required':['main'],
                      'template':"""t.section($sectionTitle(main))t.label(+PID)"""}],
    'sectionTitle':[{'required':['main'],
                     'template':"""t.titlePID(+PID)t.nameInTitle(+foreNames,+lastName)"""+\
    """t.space()t.genderSymbol(+gender)"""}],
    'mainParagraph':[{'required':['main*','father','mother'],
                      'template':"""$nameWithPIDInText(main)"""+\
    """, son of $nameWithPIDInText(father) and $nameWithPIDInText(mother),"""},
                     {'required':['main*'],
                      'template':"""$nameWithPIDInText(main)"""}],
     'nameWithPIDInText':[{'required':['main'],
                       'template':"""(+foreNames) t.firstLetterBold(+lastName)t.textPID(+PID)"""}]}
    
    @staticmethod
    def __extractRolesAndTagsFrom(roleSpecifications):
        parsedSpecifications = []
        for roleSpecification in roleSpecifications:
            role,tag = re.findall('(\w+)(.?)',roleSpecification)[0]
            parsedSpecifications.append({'role':role,'tag':tag})
        return parsedSpecifications
    
    @staticmethod
    def findGivenNameAndInput(name,candidatePeople):
        templateGroup     = WriterTemplate.__template[name].copy()
        templateCandidate = WriterTemplate()
        while len(templateGroup) > 0:
            templateDict = templateGroup.pop(0)
            templateCandidate.setupWith(templateDict,candidatePeople)
            if templateCandidate.__isComplete(): break
        return templateCandidate
    
    def getText(self):
        return self.__text
    
    def getPeople(self):
        return self.__selectedPeople
    
    def replace(self,textToReplace,replacementText):
        self.__text = self.__text.replace(textToReplace,replacementText)
    
    def setupWith(self,inputDict,candidates):
        if not 'all' in inputDict['required']:
            self.__requiredPeople = self.__extractRolesAndTagsFrom(inputDict['required']) 
            self.__selectPeopleFromCandidates(candidates)
        else:
            self.__requiredPeople = 'all'
            self.__selectedPeople = candidates
        self.__setTemplateTextWith(inputDict)    
                
    def __selectPeopleFromCandidates(self,candidates):
        self.__selectedPeople = {}
        for count,candidate in enumerate(candidates):
            if count == len(self.__requiredPeople): break
            specificationsForCandidate = self.__requiredPeople[count]
            self.__addPersonWithSpecificationsToSelection(candidate,specificationsForCandidate)
    
    def __setTemplateTextWith(self,inputDict):   
        if self.__isComplete(): self.__text = inputDict['template']
        else:                   self.__text = ''
            
    def __isComplete(self):
        return self.__requiredPeople == 'all' or\
              (len(self.__selectedPeople) == len(self.__requiredPeople))
    
    def __addPersonWithSpecificationsToSelection(self,candidate,specificationsForCandidate):
        tagForCandidate  = specificationsForCandidate['tag']
        roleForCandidate = specificationsForCandidate['role']
        if candidate.isSuitableGivenTag(tagForCandidate):
            self.__selectedPeople.update({roleForCandidate:candidate})
    
