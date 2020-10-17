import re 

class AllWriterTemplate(object):    
    def getText(self):
        return self._text
    
    def getPeople(self):
        return self._selectedPeople
    
    def replace(self,textToReplace,replacementText):
        self._text = self._text.replace(textToReplace,str(replacementText))
    
    def setupWith(self,inputDict,people):
        self._selectedPeople = people
        self._setTemplateTextWith(inputDict)
                
    def isComplete(self):
        return True   
    
    def _setTemplateTextWith(self,inputDict):   
        if self.isComplete(): self._text = inputDict['template']
        else:                 self._text = ''
            
class WriterTemplate(AllWriterTemplate):
    @staticmethod
    def extractRolesAndTagsFrom(roleSpecifications):
        parsedSpecifications = []
        for roleSpecification in roleSpecifications:
            role,tag = re.findall('(\w+)(.?)',roleSpecification)[0]
            parsedSpecifications.append({'role':role,'tag':tag})
        return parsedSpecifications
    
    def setupWith(self,inputDict,candidates):
        self._requiredPeople = self.extractRolesAndTagsFrom(inputDict['required']) 
        self.__selectPeopleFromCandidates(candidates)
        self._setTemplateTextWith(inputDict)    
                
    def isComplete(self):
        return (len(self._selectedPeople) == len(self._requiredPeople))            
            
    def __selectPeopleFromCandidates(self,candidateCollection):
        self._selectedPeople = {}
        for count,candidate in enumerate(candidateCollection):
            if count == len(self._requiredPeople): break
            specificationsForCandidate = self._requiredPeople[count]
            self.__addPersonWithSpecificationsToSelection(candidate,specificationsForCandidate)
    
    def __addPersonWithSpecificationsToSelection(self,candidate,specificationsForCandidate):
        tagForCandidate  = specificationsForCandidate['tag']
        roleForCandidate = specificationsForCandidate['role']
        if isinstance(candidate,list) or candidate.isSuitableGivenTag(tagForCandidate):
            self._selectedPeople.update({roleForCandidate:candidate})

class SelectingWriterTemplate(WriterTemplate):
    def _setTemplateTextWith(self,inputDict):   
        if self.isComplete(): 
            parameters = self.__extractInputFrom(inputDict)
            self._text = self._getTextFromMapping(*parameters)
        else: self._text = ''
    
    def _getPrimaryRequiredPerson(self):
        roleOfPrimaryRequiredPerson = self._requiredPeople[0]['role']
        return self._selectedPeople[roleOfPrimaryRequiredPerson]
    
    def _getKeyValueFromPrimaryRequiredPerson(self,keyForMapping):
        primaryRequiredPerson = self._getPrimaryRequiredPerson()
        return primaryRequiredPerson.get(keyForMapping)
    
    def __extractInputFrom(self,inputDict):
        return (inputDict[elem] for elem in self._inputKeys)
            
class KeyWriterTemplate(SelectingWriterTemplate):
    _inputKeys = ['key','map']
    
    def _getTextFromMapping(self,keyForMapping,mapping):
        keyValueForMapping = self._getKeyValueFromPrimaryRequiredPerson(keyForMapping)
        return mapping[keyValueForMapping]
    
class SelectorWriterTemplate(SelectingWriterTemplate): 
    _inputKeys = ['key','map','modifier']
    
    def _getTextFromMapping(self,keyForMapping,mapping,selector):
        roleKeys = [requiredPerson['role'] for requiredPerson in self._requiredPeople]
        if not keyForMapping in roleKeys:
            keyValueForSelector = self._getKeyValueFromPrimaryRequiredPerson(keyForMapping)
        else:
            keyValueForSelector = self._selectedPeople[keyForMapping]
        keyValueForMapping = selector(keyValueForSelector) 
        return mapping[keyValueForMapping]        
        