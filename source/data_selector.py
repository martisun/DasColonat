class DataSelector(object):    
    @staticmethod
    def createFor(requiredKeySpecifications):
        if requiredKeySpecifications.isTemplateDefined():
            return DataSelector(requiredKeySpecifications)
        else:
            return DataSelectorForMapping.createFor(requiredKeySpecifications)
    
    def __init__(self,requiredKeySpecifications):
        self._spec = requiredKeySpecifications
        self._required = self._spec.getRequiredKeySpecifications()
        self._selected = {}
    
    def isComplete(self):
        return len(self._required) == len(self._selected) 
    
    def select(self,candidateData):
        candidateData = candidateData.copy()
        for keySpecification in self._required:
            if not candidateData: break
            self.__selectElementForSpecification(candidateData.pop(0),keySpecification) 
        return self._selected
    
    def __selectElementForSpecification(self,dataElement,keySpecification):
        if isinstance(dataElement,list) or dataElement.isSuitableGivenTag(keySpecification.tag):
            self._selected.update({keySpecification.key:dataElement})     
    
    def getText(self):
        if self.isComplete(): return self._determineTemplate()       
        else:                 return ''
        
    def _determineTemplate(self):
        return self._spec.getTemplate()        

class DataSelectorForMapping(DataSelector):
    @staticmethod
    def createFor(requiredKeySpecifications):
        if requiredKeySpecifications.aModifierNeedsToBeSet():
            return DataSelectorForModifiedMapping.createFor(requiredKeySpecifications)
        else:
            return DataSelectorForMapping(requiredKeySpecifications)
    
    def _determineTemplate(self):
        keyValueForMapping = self.__getValueFromPrimaryDataKey()
        return self._spec.doMap(keyValueForMapping)
    
    def __getValueFromPrimaryDataKey(self):
        primaryRequiredData = self.__getPrimaryData()
        keyForMapping = self._spec.getKeyForMapping()
        return primaryRequiredData.get(keyForMapping)
    
    def __getPrimaryData(self):
        primaryRequiredKey = self._required[0].key
        return self._selected[primaryRequiredKey]
    
class DataSelectorForModifiedMapping(DataSelectorForMapping):
    @staticmethod
    def createFor(requiredKeySpecifications):
        if requiredKeySpecifications.isKeyForMappingRequired():
            return DataSelectorForModifiedMapping(requiredKeySpecifications)
        else:
            return DataSelectorForModifiedMappingOfPrimary(requiredKeySpecifications)
    
    def _determineTemplate(self):
        keyValueForSelector = self.__determineKeyValueForSelector()
        return self._spec.mapData(keyValueForSelector)
    
    def __determineKeyValueForSelector(self):
        keyForMapping = self._spec.getKeyForMapping()
        return self._selected[keyForMapping]
    
class DataSelectorForModifiedMappingOfPrimary(DataSelectorForModifiedMapping):
    def _determineTemplate(self):
        keyValueForSelector = self.__determineKeyValueForSelector()
        return self._spec.mapData(keyValueForSelector)
    
    def __determineKeyValueForSelector(self):
        primaryRequiredData = self.__getPrimaryData()
        keyForMapping = self._spec.getKeyForMapping()
        return primaryRequiredData.get(keyForMapping)
    
    def __getPrimaryData(self):
        primaryRequiredKey = self._required[0].key
        return self._selected[primaryRequiredKey]