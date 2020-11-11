import re

from source.writer_templates import WriterTemplate
from source.data_selector import DataSelector    

class TemplateMaker(object):
    def setupWith(self,templateSpecification,candidateData):
        self.__spec = templateSpecification
        self.__data = candidateData
        self.__isComplete = True
    
    def isComplete(self):
        return self.__isComplete                
        
    def getTemplate(self): 
        template = WriterTemplate(self.__getTemplateText())
        template.setDataTo(self.__data)
        return template
    
    def __getTemplateText(self):
        if self.__spec.hasDataSelection(): return self.__doDataSelection()
        elif self.__spec.hasMappingDefined(): return self.__spec.mapData(self.__data)
        else: return self.__spec.getTemplate()
    
    def __doDataSelection(self):
        dataSelector = DataSelector.createFor(self.__spec)
        self.__data  = dataSelector.select(self.__data)
        self.__isComplete = dataSelector.isComplete() 
        return dataSelector.getText()
        
class TemplateSpec(object):
    def __init__(self,templateDict):
        self.__dict = templateDict.copy()
        self.__setModifierInDict()
        
    def getDict(self):
        return self.__dict
    
    def setTemplateTo(self,value):
        self.__dict['template'] = value
    
    def mapData(self,data):
        key = self.__dict['modifier'](data)
        return self.doMap(key)
    
    def doMap(self,key):
        return self.__dict['map'][key]
    
    def getKeyForMapping(self):
        return self.__dict['key']
    
    def getModifier(self):
        return self.__dict['modifier']
    
    def getRequiredKeys(self):
        return self.__dict['required']
    
    def getRequiredKeySpecifications(self):
        return KeySpecification.parseList(self.__dict['required'])
    
    def getTemplate(self):
        return self.__dict['template']
    
    def __setModifierInDict(self):
        if self.aModifierNeedsToBeSet(): self.__doSetModifier()
    
    def __doSetModifier(self):
        method = KeyModifiers.getWithName(self.__dict['modifier'])
        self.__dict = {**self.__dict,'modifier':method()}
    
    def isKeyForMappingRequired(self):
        return self.getKeyForMapping() in self.getRequiredKeys()
    
    def isTemplateDefined(self):
        return 'template' in self.__dict
    
    def aModifierNeedsToBeSet(self):
        return 'modifier' in self.__dict 
    
    def hasDataSelection(self):
        return 'required' in self.__dict
    
    def hasMappingDefined(self):
        return 'map' in self.__dict 
        
class TemplateQueue(object):
    def __init__(self,templateQueueData):
        self.__data  = templateQueueData.copy()
        self.__maker = TemplateMaker() 
    
    def setupTemplateCandidateFor(self,candidateData):
        self.__maker.setupWith(self.__getNext(),candidateData)
        if self.__maker.isComplete() or self.__isEmpty(): 
            return self.__maker.getTemplate()
        else: 
            return self.setupTemplateCandidateFor(candidateData)       
    
    def __getNext(self):
        templateSpecificationData = self.__data.pop(0)
        return TemplateSpec(templateSpecificationData)
    
    def __isEmpty(self):
        return not bool(self.__data)   

class KeySpecification(object):
    __pattern = '(\w+)(.?)'
    
    @staticmethod
    def parseList(parsableTextList):
        return [KeySpecification.parse(parsableText) 
                for parsableText in parsableTextList]
    
    @staticmethod
    def parse(parsableText):
        key,tag = re.findall(KeySpecification.__pattern,parsableText)[0]
        return KeySpecification(key,tag)
    
    def __init__(self,key,tag):
        self.key = key
        self.tag = tag    
    
class LanguageTemplateCollections(object):
    @staticmethod
    def getWithLanguageTag(languageTag):
        templateCollections = {'en':EnglishTemplateCollection(),
                               'nl':DutchTemplateCollection(),
                               'de':GermanTemplateCollection()}
        return templateCollections[languageTag]      


class GeneralTemplateCollection(object):
    _generalSpecifications = {'summary':[{'template':"""
$sectionHeader(main)

$mainParagraph(main,father,mother)$lineBreak(main)$childListingIntro(main,spouse,children)$childrenListing(children)
"""}],
    'lineBreak':[{'required':['main*'],'template':"""\n\n"""}],
    'sectionHeader':[{'required':['main'],
                      'template':"""t.section($sectionTitle(main))t.label(+PID)"""}],
    'sectionTitle':[{'required':['main'],
                     'template':"""t.titlePID(+PID)t.nameInTitle(+foreNames,+lastName)"""+\
    """t.space()t.genderSymbol(+gender)"""}],     
     'childrenListing':[{'template':""" ... childrenListing ... """}],                              
     'childDescription':[{'required':['main'],'template':"""$firstNameWithPIDAndGender"""+\
                          """(main)$baptismOnly(main)"""}],
     'nameWithPIDInText':[{'required':['main'],'template':"""(+foreNames)t.space(+lastName)"""+\
                           """t.firstLetterBold(+lastName)t.textPID(+PID)"""}],
     'firstNameWithPIDAndGender':[{'required':['main'],'template':"""(+foreNames)"""+\
                  """t.space()($boldGender(main))t.space()t.textPID(+PID)"""}],
      'boldGender':[{'required':['main'],'template':"""t.bold($gender(main))"""}],
      'gender':[{'required':['main'],'template':"""t.genderSymbol(+gender)"""}]}
    def __init__(self):
        self.__dataDict = {**self._generalSpecifications,**self._languageSpecificSpecifications}
    
    def setupTemplateQueueWithName(self,name):
        return TemplateQueue(self.__dataDict[name])  

class EnglishTemplateCollection(GeneralTemplateCollection):
    _languageSpecificSpecifications =\
    {'mainParagraph':[{'required':['main','father','mother'],
                       'template':"""$nameWithPIDInText(main) is a $child(main) of $nameWithPIDInText(father) and $nameWithPIDInText(mother)."""},
                      {'required':['main*','father','mother'],
                       'template':"""$nameWithPIDInText(main)"""+\
    """, son of $nameWithPIDInText(father) and $nameWithPIDInText(mother),$baptismOnly(main)"""},
                      {'required':['main*'],'template':"""$nameWithPIDInText(main)$baptismOnly(main)"""}],
     'childListingIntro':[{'required':['father','mother','children'],'key':'children',
                           'modifier':'lengthOneOrMore',
               'map':{1:"""$FromARelationshipOfCouple(father,mother) was brought forth:""",
                      2:"""$FromARelationshipOfCouple(father,mother) were brought forth:"""}}],
     'FromARelationshipOfCouple':[{'required':['father','mother'],'template':"""From a relationship between $nameWithPIDInText(father) and $nameWithPIDInText(mother)"""}],
     'baptismOnly':[{'required':['main'],'template':""" was baptised $onTheDate(main)"""+\
                     """$beforeTheChurches(main) at $town(main)."""}],
     'onTheDate':[{'required':['main'],
                   'template':"""on the $dayOrdinal(main) $tmp(main)"""}],
     'tmp':[{'required':['main'],'template':"""of $month(+month) (+year)"""}],
     'dayOrdinal':[{'required':['main'],'key':'day','modifier':'ordinalSelector',
                    'map':{0:'$dayth(main)',1:'$dayst(main)',2:'$dayth(main)'}}],
     'dayth':[{'required':['main'],'template':"""(+day)t.superScript(th)"""}],
     'dayst':[{'required':['main'],'template':"""(+day)t.superScript(st)"""}],
     'month':[{'modifier':'toInt','map':{0:'',2:'February',5:'May',6:'June',7:'July',
                                         8:'August',9:'September',12:'December'}}],
     'child':[{'required':['main'],'key':'gender','map':{'m':'son','':'child'}}],
     'town':[{'template':"""Freren"""}],
     'beforeTheChurches':[{'required':['main'],'key':'denom','modifier':'primalListSelector',
                           'map':{'rc':""" before the catholic church$ofTheNamedParish(main)$andChurchBoth(main)""",'ref':""" before the reformed church$ofTheNamedParish(main)$andChurchBoth(main)""",'':''}}],
     'ofTheNamedParish':[{'required':['main'],'key':'denom','modifier':'primalListSelector',
                          'map':{'rc':' of the t.italic(St. Vitus) parish','ref':'','':''}}],
     'andChurchBoth':[{'required':['main'],'key':'denom','modifier':'secondaryListSelector',
                       'map':{'ref':' and the reformed church, both','rc':'','':''}}]}

class DutchTemplateCollection(GeneralTemplateCollection):
    _languageSpecificSpecifications =\
    {'mainParagraph':[{'required':['main*','father','mother'],
                       'template':"""$nameWithPIDInText(main)"""+\
    """, $child(main) van $nameWithPIDInText(father) en $nameWithPIDInText(mother),"""},
                       {'required':['main','father','mother'],
                       'template':"""$nameWithPIDInText(main) is een $child(main) van $nameWithPIDInText(father) en $nameWithPIDInText(mother)."""},
                       {'required':['main*'],'template':"""$nameWithPIDInText(main)"""}],
     'onTheDate':[{'required':['main'],
                   'template':"""op (+day) december (+year)"""}],
     'month':[{'required':['main'],'key':'month',
               'map':{2:'februari',5:'mei',6:'juni',7:'juli',12:'december'}}],
     'child':[{'required':['main'],'key':'gender','map':{'m':'zoon','':'kind'}}]}

class GermanTemplateCollection(GeneralTemplateCollection):
    _languageSpecificSpecifications =\
    {'mainParagraph':[{'required':['main*','father','mother'],
                          'template':"""$nameWithPIDInText(main)"""+\
    """, Sohn von $nameWithPIDInText(father) und $nameWithPIDInText(mother),"""},
                      {'required':['main','father','mother'],
                       'template':"""$nameWithPIDInText(main) ist ein $child(main) von $nameWithPIDInText(father) und $nameWithPIDInText(mother)."""},
                      {'required':['main*'],'template':"""$nameWithPIDInText(main)"""}],
     'onTheDate':[{'required':['main'],
                   'template':"""am (+day). Dezember (+year)"""}],
     'month':[{'required':['main'],'key':'month',
               'map':{2:'Februar',5:'Mai',6:'Juni',7:'Juli',12:'Dezember'}}],
     'child':[{'required':['main'],'key':'gender','map':{'m':'Sohn','':'Kind'}}]}
    

class KeyModifiers(object):
    @staticmethod
    def getWithName(modifierName):
        return getattr(KeyModifiers(),modifierName)
        
    @staticmethod
    def ordinalSelector():
        def getLastDigit(x):
            if x == '': return 0
            else:       return int(x)%10
        selectFirst  = lambda x: min(2,getLastDigit(x))
        return selectFirst
    
    @staticmethod
    def toInt():
        def toInt(x):
            if x == '': return 0
            else:       return int(x)
        return toInt  
    
    @staticmethod
    def primalListSelector():
        return KeyModifiers.__listSelector(0)  
    
    @staticmethod
    def secondaryListSelector():
        return KeyModifiers.__listSelector(1)  
    
    @staticmethod
    def __listSelector(index):
        def listSelector(x):
            if index < len(x): return x[index]
            else:              return ''
        return listSelector  
    
    @staticmethod
    def lengthOneOrMore():
        oneOrMore = lambda x: min(len(x),2)
        return oneOrMore        