import re

from source.latex_templater import LatexTemplater

class WriterTemplate(object): 
    blankArgument    = '+blank'
    __subWriterPattern = ['(\$(\w+)\(([\,\w]+)\))',
                          '(\$(\w+)\(\+([\,\w]+)\))']
    
    @staticmethod
    def makeListingOf(templateItems):
        return LatexTemplater.compileListingOf(templateItems)
    
    def __init__(self,text):
        self.__text = text
        self.__mainDataTags = []
    
    def getText(self):
        return LatexTemplater.replaceSpecialCharacters(self.__text)
    
    def getData(self):
        return self.__selected
    
    def getMainDataTags(self):
        return self.__mainDataTags
    
    def getSubWriterSpecifications(self):
        specifications = []
        for pattern in self.__subWriterPattern:
            specifications += self.__parseSubWriterSpecificationWithPattern(pattern)
        return specifications
    
    def __parseSubWriterSpecificationWithPattern(self,pattern):
        return re.findall(pattern,self.__text)
    
    def replaceByTemplate(self,textToReplace,replacement):
        self.replaceText(textToReplace,replacement.__text)
    
    def replaceBlankBy(self,replacementText):
        self.replaceText(self.blankArgument,replacementText)
    
    def replaceByBlank(self,textToReplace):
        self.replaceText(textToReplace,self.blankArgument)
    
    def replaceText(self,textToReplace,replacementText):
        self.__text = self.__text.replace(textToReplace,str(replacementText))

    def doAllReplacements(self):
        self.__doReplacements()
        self.__doSubReplacements()
    
    def __doReplacements(self):
        specifications = self.__extractSpecifications('(\((\w+)\))')
        self.__replaceSpecifications(specifications) 
        
    def __doSubReplacements(self):
        specifications = self.__extractSpecifications('(\(\+(\w+)\))')
        self.__replaceSubSpecifications(specifications)  

    def __extractSpecifications(self,pattern):
        return re.findall(pattern,self.__text)            
    
    def __replaceSpecifications(self,specifications):
        for specification in specifications:
            self.__replaceSpecification(*specification)
    
    def __replaceSubSpecifications(self,specifications):
        for specification in specifications:
            self.__replaceSingleSubSpecification(*specification)
    
    def __replaceSingleSubSpecification(self,blank,parameter):
        mainTag = self.__mainDataTags[0]
        value = self.__selected[mainTag].get(parameter)
        self.replaceText(blank,value)
        
    def __replaceSpecification(self,blank,parameter):
        if parameter in self.__mainDataTags:    
            value = self.__selected[parameter]
            self.replaceText(blank,value) 
    
    def setDataTo(self,data):
        if isinstance(data,dict): self.__selected = {el:data[el].getData() for el in data}
        else: self.__selected = data.getData()
        
    def setMainDataTo(self,mainDataKeySpecs):
        mainDataTags = [elem.key for elem in mainDataKeySpecs]
        self.__mainDataTags = mainDataTags
        
    def __repr__(self):
        return 'WriterTemplate[text=%s,data=%s]'%(self.__text,self.__selected.keys())