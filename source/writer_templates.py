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
    
    def setDataTo(self,data):
        self.__selected = data
        
    def setMainDataTo(self,mainDataTags):
        self.__mainDataTags = mainDataTags
        
    def __repr__(self):
        return 'WriterTemplate[text=%s,data=%s]'%(self.__text,self._selected.keys())