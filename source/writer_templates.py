import re 

class AllWriterTemplate(object):    
    def getText(self):
        return self._text
    
    def getPeople(self):
        return self._selectedPeople
    
    def replace(self,textToReplace,replacementText):
        self._text = self._text.replace(textToReplace,replacementText)
    
    def setupWith(self,inputDict,people):
        self._selectedPeople = people
        self._text = inputDict['template']  
                
    def isComplete(self):
        return True           
    
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
        self.__setTemplateTextWith(inputDict)    
                
    def isComplete(self):
        return (len(self._selectedPeople) == len(self._requiredPeople))            
            
    def __selectPeopleFromCandidates(self,candidates):
        self._selectedPeople = {}
        for count,candidate in enumerate(candidates):
            if count == len(self._requiredPeople): break
            specificationsForCandidate = self._requiredPeople[count]
            self.__addPersonWithSpecificationsToSelection(candidate,specificationsForCandidate)
    
    def __setTemplateTextWith(self,inputDict):   
        if self.isComplete(): self._text = inputDict['template']
        else:                 self._text = ''
    
    def __addPersonWithSpecificationsToSelection(self,candidate,specificationsForCandidate):
        tagForCandidate  = specificationsForCandidate['tag']
        roleForCandidate = specificationsForCandidate['role']
        if candidate.isSuitableGivenTag(tagForCandidate):
            self._selectedPeople.update({roleForCandidate:candidate})
    
