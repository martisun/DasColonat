import re

from source.latex_templater import LatexTemplater

class Writer(object): 
    __blankedArgument = '+blank'
    
    @staticmethod
    def extractFullTemplaterSpecificationsFrom(templateText):
        return re.findall('(t\.(\w+)\(([\+\w+\,]+)?\))',templateText)
    
    @staticmethod
    def extractBlankedTemplaterSpecificationsFrom(templateText):
        return re.findall('(t\.(\w+)\(\+blank\))',templateText)[0]
    
    @staticmethod
    def extractParametersFromTemplaterArguments(arguments):
        return re.findall('\+(\w+)',arguments)
    
    @staticmethod
    def parse(templateText):
        specifications = re.findall('(\$(\w+)\((\w+)\))',templateText)
        return [Writer(specification) for specification in specifications]   
    
    def __init__(self,specification):
        blank,name,required = specification
        self.__blank        = blank
        self.__templater    = LatexTemplater()
        self.__templateText = WriterTemplates.get(name) 
        self.__required     = [required]
    
    def getBlank(self):
        return self.__blank
    
    def write(self,people):
        requiredPeople = self.__selectRequiredPeopleFrom(people)
        self.__replaceSubWriterTemplates(requiredPeople)
        self.__replaceTemplaterCalls(requiredPeople)
        return self.__templateText 

    def __applyTemplaterWithValueToBlankIn(self,argument,superTemplateText):
        blank,method     = self.extractBlankedTemplaterSpecificationsFrom(superTemplateText)
        blankReplacement = self.__templater.evaluate(method,[argument])
        return superTemplateText.replace(blank,blankReplacement)
    
    def __blankOutIn(self,superTemplateText):
        return superTemplateText.replace(self.__blank,self.__blankedArgument)    
    
    def __replaceSubWriterTemplates(self,people):
        for subWriter in self.parse(self.__templateText):
            self.__templateText = subWriter.__writeIntoTemplateWith(self.__templateText,people)
    
    def __replaceTemplaterCalls(self,people):
        specifications = self.extractFullTemplaterSpecificationsFrom(self.__templateText)
        for blank,method,arguments in specifications:
            blankReplacement    = self.__determineTemplaterBlankReplacement(method,arguments,people) 
            self.__templateText = self.__templateText.replace(blank,blankReplacement)
    
    def __determineTemplaterBlankReplacement(self,method,arguments,people):
        parameters = self.extractParametersFromTemplaterArguments(arguments)
        if not (len(arguments) > 0 and len(parameters) == 0):
            values = people['main'].get(parameters)    
            return self.__templater.evaluate(method,values)
        else:
            return self.__templater.evaluate(method,[arguments])
    
    def __selectRequiredPeopleFrom(self,people):
        return {role:people[role] for role in self.__required}
    
    def __writeIntoTemplateWith(self,superTemplateText,people):
        superTemplateText = self.__blankOutIn(superTemplateText)
        blankReplacement  = self.write(people) 
        return self.__applyTemplaterWithValueToBlankIn(blankReplacement,superTemplateText)
        

class WriterTemplates(object):
    __template = {'summary':"""
$sectionHeader(main)

""",'sectionHeader':"""t.section($sectionTitle(main))t.label(+PID)""",
    'sectionTitle':"""t.titlePID(+PID)t.nameInTitle(+foreNames,+lastName)"""+\
    """t.space()t.genderSymbol(+gender)"""}
    
    @staticmethod
    def get(name):
        return WriterTemplates.__template[name]
