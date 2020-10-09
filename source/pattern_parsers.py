import re

class PatternParser(object):    
    @staticmethod
    def extractParametersFromArguments(arguments):
        return re.findall('(\(\+(\w+)\))',arguments)             
            
class TemplaterPatternParser(PatternParser):
    blankedArgument = '+blank'
    
    @staticmethod
    def extractParameterNamesFromArguments(arguments):
        return re.findall('\+(\w+)',arguments) 
    
    @staticmethod
    def extractFullSpecsFrom(templateText):
        return re.findall('(t\.(\w+)\(([\+\w+\,\s\.]+)?\))',templateText)
    
    @staticmethod
    def extractBlankedSpecsFrom(templateText):
        return re.findall('(t\.(\w+)\(\+blank\))',templateText)