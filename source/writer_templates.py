import re 

class BaseWriterTemplate(object):
    def __init__(self,inputDict):
        self._inputDict = inputDict
    
    def getText(self):
        return self._text
    
    def isComplete(self):
        return True   

class AllWriterTemplate(BaseWriterTemplate): 
    blankArgument = '+blank'
    
    def getPeople(self):
        return self._selectedPeople
    
    def replaceBlankBy(self,replacementText):
        self.replace(self.blankArgument,replacementText)
    
    def replaceByBlank(self,textToReplace):
        self.replace(textToReplace,self.blankArgument)
    
    def replace(self,textToReplace,replacementText):
        self._text = self._text.replace(textToReplace,str(replacementText))
    
    def setPeopleTo(self,people):
        self._selectedPeople = people
        self._text = self._inputDict['template']

class ModifiedMapTemplate(BaseWriterTemplate):
    def setPeopleTo(self,people):
        key = self._inputDict['modifier'](people)
        self._text = self._inputDict['map'][key]            
            
class WriterTemplate(AllWriterTemplate):    
    def setPeopleTo(self,people):
        self._dataSelector = DataSelector(self._inputDict['required'])
        self._dataSelector.select(people)
        self._setTemplateTextWith(self._inputDict)    
    
    def getPeople(self):
        return self._dataSelector.getSelected()
    
    def _setTemplateTextWith(self,inputDict):
        if self._dataSelector.isComplete(): self._text = inputDict['template']
        else:                               self._text = ''
    
    def isComplete(self):
        return self._dataSelector.isComplete()             
            
class SelectingWriterTemplate(WriterTemplate):
    def _setTemplateTextWith(self,inputDict):   
        if self._dataSelector.isComplete(): 
            parameters = self.__extractInputFrom(inputDict)
            self._text = self._getTextFromMapping(*parameters)
        else: self._text = ''
    
    def __extractInputFrom(self,inputDict):
        return (inputDict[elem] for elem in self._inputKeys)
            
class KeyWriterTemplate(SelectingWriterTemplate):
    _inputKeys = ['key','map']
    
    def _getTextFromMapping(self,keyForMapping,mapping):
        keyValueForMapping = self._dataSelector.getValueFromPrimaryDataKey(keyForMapping)
        return mapping[keyValueForMapping]
    
class SelectorWriterTemplate(SelectingWriterTemplate): 
    _inputKeys = ['key','map','modifier']
    
    def _getTextFromMapping(self,keyForMapping,mapping,selector):
        if not keyForMapping in self._inputDict['required']:
            keyValueForSelector = self._dataSelector.getValueFromPrimaryDataKey(keyForMapping)
        else:
            selectedPeople = self._dataSelector.getSelected()
            keyValueForSelector = selectedPeople[keyForMapping]   
        keyValueForMapping = selector(keyValueForSelector) 
        return mapping[keyValueForMapping]    

class DataSelector(object):
    __keySpecificationPattern = '(\w+)(.?)'
    
    def __init__(self,requiredKeySpecifications):
        self.__required = self.__parseKeySpecifications(requiredKeySpecifications)
        self.__selected = {}
    
    def getSelected(self):
        return self.__selected
    
    def isComplete(self):
        return len(self.__required) == len(self.__selected) 
    
    def getValueFromPrimaryDataKey(self,keyForMapping):
        primaryRequiredData = self.__getPrimaryData()
        return primaryRequiredData.get(keyForMapping)
    
    def select(self,candidateData):
        candidateData = candidateData.copy()
        for keySpecification in self.__required:
            if not candidateData: break
            self.__selectElementForSpecification(candidateData.pop(0),keySpecification) 
    
    def __getPrimaryData(self):
        primaryRequiredKey = self.__required[0]['key']
        return self.__selected[primaryRequiredKey]
    
    def __selectElementForSpecification(self,dataElement,keySpecification):
        tag  = keySpecification['tag']; key = keySpecification['key']
        if isinstance(dataElement,list) or dataElement.isSuitableGivenTag(tag):
            self.__selected.update({key:dataElement}) 
        
    def __parseKeySpecifications(self,keySpecifications):
        return [self.__parseKeySpecification(keySpecification) 
                for keySpecification in keySpecifications]
    
    def __parseKeySpecification(self,keySpecification):
        key,tag = re.findall(self.__keySpecificationPattern,keySpecification)[0]
        return {'key':key,'tag':tag}    
    