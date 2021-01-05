from source.writer_templates import WriterTemplate
from source.record_data import WriterData, KeySpecification

class WriterTemplateMakerBuilder(object):    
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
            return WriterTemplateMaker(self.__spec)
        
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

class WriterTemplateMaker(object):
    def __init__(self,writerTemplateSpecifications):
        self._spec = writerTemplateSpecifications
    
    def select(self,candidateData):
        self._selected = candidateData
        
    def getWriterTemplate(self):
        writerTemplate = WriterTemplate(self.getText())
        writerTemplate.setDataTo(self._selected)
        return writerTemplate
    
    def isComplete(self):
        return True
    
    def getText(self):
        return self._getTemplateText()
    
    def _getTemplateText(self):
        return self._spec.getTemplate()

class MappingWriterTemplateMaker(WriterTemplateMaker):
    def select(self,candidateData):
        self.__text = self._spec.mapDataForCandidate(candidateData)
        super().select(candidateData)
    
    def _getTemplateText(self):
        return self.__text    
    
class SelectiveWriterTemplateMaker(WriterTemplateMaker):        
    def __init__(self,writerTemplateSpecifications):
        super().__init__(writerTemplateSpecifications)
        self._required = KeySpecification.setupFrom(self._spec)
        self._selected = WriterData.makeFrom({})
    
    def isComplete(self):
        return len(self._required) == len(self._selected) 
    
    def select(self,candidateData):
        self.__setupRequiredKeyedData(candidateData)
        self._selected.selectData(self._required)
        
    def __setupRequiredKeyedData(self,candidateData):
        candidateData = candidateData.copy()
        for keyedData in self._required: 
            keyedData.setWriterData(candidateData)
        
    def getText(self):
        if self.isComplete(): return super().getText()       
        else:                 return ''
    
    def getWriterTemplate(self):
        writerTemplate = WriterTemplate(self.getText())
        writerTemplate.setDataTo(self._selected)
        writerTemplate.setMainDataTo(self._required)
        return writerTemplate 
    
class SubMappingWriterTemplateMaker(SelectiveWriterTemplateMaker):    
    def _getTemplateText(self):
        keyValueForMapping = self.__getValueFromPrimaryDataKey()
        return self._spec.doMap(keyValueForMapping)
    
    def __getValueFromPrimaryDataKey(self):
        primaryRequiredData = self.__getPrimaryData()
        keyForMapping = self._spec.getKeyForMapping()
        return primaryRequiredData.get(keyForMapping)
    
    def __getPrimaryData(self):
        primaryRequiredKey = self._required[0].key
        return self._selected.selectTag(primaryRequiredKey)
    
class ModifiedSubMappingWriterTemplateMaker(SubMappingWriterTemplateMaker):    
    def _getTemplateText(self):
        keyValueForSelector = self.__determineKeyValueForSelector()
        return self._spec.mapData(keyValueForSelector)
    
    def __determineKeyValueForSelector(self):
        keyForMapping = self._spec.getKeyForMapping()
        print('l.126 template_maker.py refactoring')
        return self._selected.selectTag(keyForMapping).getData()
    
class ModifiedSubMappingWriterTemplateMakerOfPrimary(ModifiedSubMappingWriterTemplateMaker):
    def _getTemplateText(self):
        keyValueForSelector = self.__determineKeyValueForSelector()
        return self._spec.mapData(keyValueForSelector)
    
    def __determineKeyValueForSelector(self):
        primaryRequiredData = self.__getPrimaryData()
        keyForMapping = self._spec.getKeyForMapping()
        return primaryRequiredData.get(keyForMapping)
    
    def __getPrimaryData(self):
        primaryRequiredKey = self._required[0].key
        print('l.140 template_maker.py refactoring')
        return self._selected.selectTag(primaryRequiredKey).getData()