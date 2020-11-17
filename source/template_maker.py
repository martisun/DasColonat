from source.writer_templates import WriterTemplate

class TemplateMaker(object):    
    def getWriterTemplateMakerFor(self,templateSpecification):
        self.__spec = templateSpecification
        dataSelector = self.__selectWriterTemplateMaker()
        return dataSelector
    
    def __selectWriterTemplateMaker(self):
        if self.__spec.hasDataSelection(): 
            return self.__selectSelectiveWriterTemplateMaker()
        elif self.__spec.hasMappingDefined(): 
            return MappingWriterTemplateMaker(self.__spec)
        else: 
            return TrivialWriterTemplateMaker(self.__spec)
        
    def __selectSelectiveWriterTemplateMaker(self):
        if self.__spec.isTemplateDefined():
            return SelectiveWriterTemplateMaker(self.__spec)
        else:
            return self.__selectMappingWriterTemplateMaker()
        
    def __selectMappingWriterTemplateMaker(self):
        if self.__spec.aModifierNeedsToBeSet():
            return self.__selectModifiedMappingWriterTemplateMaker()
        else:
            return SubMappingWriterTemplateMaker(self.__spec)
        
    def __selectModifiedMappingWriterTemplateMaker(self):
        if self.__spec.isKeyForMappingRequired():
            return ModifiedSubMappingWriterTemplateMaker(self.__spec)
        else:
            return ModifiedSubMappingWriterTemplateMakerOfPrimary(self.__spec)    

class TrivialWriterTemplateMaker(object):
    def __init__(self,writerTemplateSpecifications):
        self._spec = writerTemplateSpecifications
    
    def select(self,candidateData):
        self._selected = candidateData
    
    def getWriterTemplate(self):
        writerTemplate = WriterTemplate(self._getTemplateText())
        writerTemplate.setDataTo(self._selected)
        return writerTemplate
    
    def isComplete(self):
        return True
    
    def _getTemplateText(self):
        return self._spec.getTemplate()
        
class MappingWriterTemplateMaker(TrivialWriterTemplateMaker):
    def select(self,candidateData):
        print('l.55 candidateData:',candidateData)
        print('.. spec:',self._spec)
        if isinstance(candidateData,list): 
            self.__text = self._spec.mapData(candidateData[0])
        else: self.__text = self._spec.mapData(candidateData)
        self._selected = candidateData
    
    def _getTemplateText(self):
        return self.__text

class SelectiveWriterTemplateMaker(object):        
    def __init__(self,requiredKeySpecifications):
        self._spec = requiredKeySpecifications
        self._required = self._spec.getRequiredKeySpecifications()
        self._selected = {}
    
    def isComplete(self):
        return len(self._required) == len(self._selected) 
    
    def select(self,candidateData):
        print('l.71 candidateData:',candidateData)
        print('... self._spec:',self._spec)
        print('... self._required:',self._required)
        if not isinstance(candidateData,int) and not isinstance(candidateData,str):
            candidateData = candidateData.copy() 
        for keySpecification in self._required:
            if isinstance(candidateData,list) and not candidateData: break
            if not isinstance(candidateData,int) and not isinstance(candidateData,str):
                self.__selectElementForSpecification(candidateData.pop(0),keySpecification) 
            else:
                self._selected.update({keySpecification.key:candidateData})
    
    def __selectElementForSpecification(self,dataElement,keySpecification):
        if isinstance(dataElement,list) or dataElement.isSuitableGivenTag(keySpecification.tag):
            self._selected.update({keySpecification.key:dataElement})     
    
    def getText(self):
        if self.isComplete(): return self._determineTemplate()       
        else:                 return ''
    
    def getWriterTemplate(self):
        writerTemplate = WriterTemplate(self.getText())
        writerTemplate.setDataTo(self._selected)
        return writerTemplate
    
    def _determineTemplate(self):
        return self._spec.getTemplate()        

class SubMappingWriterTemplateMaker(SelectiveWriterTemplateMaker):    
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
    
class ModifiedSubMappingWriterTemplateMaker(SubMappingWriterTemplateMaker):    
    def _determineTemplate(self):
        keyValueForSelector = self.__determineKeyValueForSelector()
        return self._spec.mapData(keyValueForSelector)
    
    def __determineKeyValueForSelector(self):
        keyForMapping = self._spec.getKeyForMapping()
        return self._selected[keyForMapping]
    
class ModifiedSubMappingWriterTemplateMakerOfPrimary(ModifiedSubMappingWriterTemplateMaker):
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