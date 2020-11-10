# add children from if-statements


class DataSelector(object):    
    def __init__(self,requiredKeySpecifications):
        self.__spec = requiredKeySpecifications
        self.__required = self.__spec.getRequiredKeySpecifications()
        self.__selected = {}
    
    def isComplete(self):
        return len(self.__required) == len(self.__selected) 
    
    def select(self,candidateData):
        candidateData = candidateData.copy()
        for keySpecification in self.__required:
            if not candidateData: break
            self.__selectElementForSpecification(candidateData.pop(0),keySpecification) 
        return self.__selected
    
    def __selectElementForSpecification(self,dataElement,keySpecification):
        if isinstance(dataElement,list) or dataElement.isSuitableGivenTag(keySpecification.tag):
            self.__selected.update({keySpecification.key:dataElement})     
    
    def getText(self):
        if self.isComplete(): return self.__determineTemplate()            
        else:                 return ''
    
    def __determineTemplate(self):
        if self.__spec.isTemplateDefined():
            return self.__spec.getTemplate()
        else:
            return self.__determineTemplateGivenMapping()
    
    def __determineTemplateGivenMapping(self):
        if self.__spec.aModifierNeedsToBeSet():
            return self.__determineTemplateGivenSelector()
        else:
            return self.__determineTemplateFromPrimaryDataKey()
    
    def __determineTemplateGivenSelector(self):
        keyValueForSelector = self.__determineKeyValueForSelector()
        return self.__spec.mapData(keyValueForSelector)
    
    def __determineTemplateFromPrimaryDataKey(self):
        keyValueForMapping = self.__getValueFromPrimaryDataKey()
        return self.__spec.doMap(keyValueForMapping)
    
    def __determineKeyValueForSelector(self):
        if self.__spec.isKeyForMappingRequired(): 
            keyForMapping = self.__spec.getKeyForMapping()
            return self.__selected[keyForMapping]
        else:
            return self.__getValueFromPrimaryDataKey()
    
    def __getValueFromPrimaryDataKey(self):
        primaryRequiredData = self.__getPrimaryData()
        keyForMapping = self.__spec.getKeyForMapping()
        return primaryRequiredData.get(keyForMapping)
    
    def __getPrimaryData(self):
        primaryRequiredKey = self.__required[0].key
        return self.__selected[primaryRequiredKey]