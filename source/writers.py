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
            
class AllWriter(Writer):
    def __init__(self,blank,name):
        super().__init__(blank,name)
        self._replacers = [SubWriterReplacer(self),ParameterReplacer()]        
        
class SelectiveWriter(AllWriter):      
    def __init__(self,blank,name,arguments):
        super().__init__(blank,name)
        self.__selector   = RoleSelector(arguments)
    
    def write(self,people):
        peopleCandidates = self.__selector.selectPeopleFrom(people)
        return super().write(peopleCandidates) 
    
class TemplaterWriter(SelectiveWriter):    
    def __init__(self,*specification):
        super().__init__(*specification)
        self._replacers.insert(0,SimpleTemplaterCallReplacer())
        self.__blankReplacer = BlankTemplaterCallReplacer(self)
        
    def writeIntoTemplateWith(self,superTemplate):
        superTemplate.replaceByBlank(self._blank)
        self.__blankReplacer.doReplacementsTo(superTemplate)     

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
            template.replace(blank,blankReplacement)  
    
    def __determineBlankReplacement(self,method,arguments,template):
        people      = template.getPeople()
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
        argument = self.__parentWriter.write(template.getPeople())
        if specifications: 
            blank,method = specifications.pop()
            argument     = self._templater.evaluate(method,[argument])
            template.replace(blank,argument) 
        else: 
            template.replaceBlankBy(argument)       
    
    def _extractSpecificationsFromTemplate(self,template):
        blankArgument = re.escape(template.blankArgument)
        return super()._extractSpecificationsFromTemplate(template,blankArgument)
    
class RoleSelector(object):
    def __init__(self,roles):
        self.__inputRoles = roles
        
    def selectPeopleFrom(self,people):
        peopleCandidates = []        
        for inputRole in self.__inputRoles:
            if inputRole in people: peopleCandidates.append(people[inputRole])
            else:                   peopleCandidates
        return peopleCandidates                         