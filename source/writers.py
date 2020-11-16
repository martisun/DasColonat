import re

from source.latex_templater import LatexTemplater

class Writer(object):
    def __init__(self,blank,queue):
        self._blank         = blank
        self._replacers     = []
        self.__queue        = queue
    
    def parseTemplate(self,template,people):
        return self.__maker.parse(template.getText(),people)
    
    def setMakerTo(self,maker):
        self.__maker = maker
        
    def write(self,people):
        template = self.__queue.setupTemplateCandidateFor(people)
        for replacer in self._replacers:
            replacer.doReplacementsTo(template)
        return LatexTemplater.replaceSpecialCharacters(template.getText())   
    
    def writeIntoTemplateWith(self,superTemplate):
        blankReplacement  = self.write(superTemplate.getPeople()) 
        superTemplate.replace(self._blank,blankReplacement)     
            
class AllWriter(Writer):
    def __init__(self,blank,queue):
        super().__init__(blank,queue)
        self._replacers = [SubWriterReplacer(self),ParameterReplacer()]        
        
class SelectiveWriter(AllWriter):      
    def __init__(self,blank,queue,arguments):
        super().__init__(blank,queue)
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
    def __init__(self,blank,queue,arguments):
        self.__templater = LatexTemplater()
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
        superTemplate.replace(self.__blank,blankReplacement)
    
    def subWriterInListing(self,people):
        listingTexts = [self.__compileListingElementOf(person) for person in people]
        return self.__templater.compileListingOf(listingTexts)

    def __compileListingElementOf(self,person):
        template = self.__queue.setupTemplateCandidateFor(person)
        subWriter = self.__writerMaker.parse(template.getText(),'')[0]
        return subWriter.write({'main':person})        
        
class SubWriterReplacer(object):  
    def __init__(self,parentWriter):
        self.__parent = parentWriter    
    
    def doReplacementsTo(self,template):
        people = template.getData()
        for subWriter in self.__parent.parseTemplate(template,people):
            subWriter.writeIntoTemplateWith(template)           

class ParameterReplacer(object):
    def doReplacementsTo(self,template):
        specifications = self.__extractSpecificationsFromTemplate(template)
        for blank,parameter in specifications:
            people = template.getData()
            print('writers.py l.92 parameter:',parameter)
            print('.. template:',template)
            print('.. people.get(day):',people)
            if 'main' in people:
                value = people['main'].get(parameter)
            else:
                value = people['day'].get('day')
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
        argument = self.__parentWriter.write(template.getData())
        if specifications: 
            self.__replaceSpecificationsInTemplate(template,specifications,argument)
        else: 
            template.replaceBlankBy(argument)       
    
    def __replaceSpecificationsInTemplate(self,template,specifications,argument):
        blank,method = specifications.pop()
        argument     = self._templater.evaluate(method,[argument])
        template.replace(blank,argument)
    
    def _extractSpecificationsFromTemplate(self,template):
        blankArgument = re.escape(template.blankArgument)
        return super()._extractSpecificationsFromTemplate(template,blankArgument)
    
class RoleSelector(object):
    def __init__(self,roles):
        self.__inputRoles = roles
        
    def selectPeopleFrom(self,people):
        peopleCandidates = self.__selectPeopleAtSameLevel(people)
        if not peopleCandidates and self.__inputRoles:
            return self.__selectDataAtSubLevel(people)
        return peopleCandidates
    
    def __selectPeopleAtSameLevel(self,people):
        return [people[inputRole] for inputRole in self.__inputRoles if inputRole in people]
    
    def __selectDataAtSubLevel(self,people):
        return people['main'].data[self.__inputRoles[0]]
        
    
    
    
        