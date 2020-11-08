import re

class DataSelector(object):
    __keySpecificationPattern = '(\w+)(.?)'
    
    def __init__(self,requiredKeySpecifications):
        self.__inputDict = requiredKeySpecifications
        self.__required = self.__parseKeySpecifications(requiredKeySpecifications['required'])
        self.__selected = {}
    
    def getSelected(self):
        return self.__selected
    
    def isComplete(self):
        return len(self.__required) == len(self.__selected) 
    
    def select(self,candidateData):
        candidateData = candidateData.copy()
        for keySpecification in self.__required:
            if not candidateData: break
            self.__selectElementForSpecification(candidateData.pop(0),keySpecification) 
    
    def getText(self):   
        if self.isComplete():
            if 'template' in self.__inputDict:
                return self.__inputDict['template']
            else:
                keyForMapping = self.__inputDict['key']
                mapping       = self.__inputDict['map']
                if 'modifier' in self.__inputDict:
                    selector = self.__inputDict['modifier']
                    if not keyForMapping in self.__inputDict['required']:
                        keyValueForSelector = self.__getValueFromPrimaryDataKey(keyForMapping)
                    else:
                        keyValueForSelector = self.__selected[keyForMapping]   
                    keyValueForMapping = selector(keyValueForSelector) 
                else:
                    keyValueForMapping = self.__getValueFromPrimaryDataKey(keyForMapping)
                return mapping[keyValueForMapping]
        else: return ''
        
    def __getValueFromPrimaryDataKey(self,keyForMapping):
        primaryRequiredData = self.__getPrimaryData()
        return primaryRequiredData.get(keyForMapping)        
    
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