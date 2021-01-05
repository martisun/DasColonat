import re

from source.template_maker import WriterTemplateMakerBuilder
        
class TemplateSpec(object):
    def __init__(self,templateDict):
        self.__dict = templateDict.copy()
        self.__setModifierInDict()
        
    def getDict(self):
        return self.__dict
    
    def setTemplateTo(self,value):
        self.__dict['template'] = value
    
    def mapDataForCandidate(self,candidateData):
        candidateData = candidateData.getMainData()
        return self.mapData(candidateData.getData())
    
    def mapData(self,data):
        key = self.__dict['modifier'](data)
        return self.doMap(key)
    
    def doMap(self,key):
        return self.__dict['map'][key]
    
    def getKeyForMapping(self):
        return self.__dict['key']
    
    def getLength(self):
        return self.__dict['length']
    
    def getModifier(self):
        return self.__dict['modifier']
    
    def getRequiredKeys(self):
        return self.__dict['required']
    
#    def getRequiredKeySpecifications(self):
#        listOfKeySpecs = KeySpecification.parseList(self.__dict['required'])
#        for el in listOfKeySpecs:
#            el.setDesiredLengthSpec(self)
#        return listOfKeySpecs
    
    def getTemplate(self):
        return self.__dict['template']
    
    def hasNonTrivialLength(self):
        return 'length' in self.__dict
    
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
    
    def __repr__(self):
        return 'TemplateSpec[%s]'%(str(self.__dict))
        
class TemplateQueue(object):
    def __init__(self,templateQueueData):
        self.__queueData  = templateQueueData.copy()
        self.__builder    = WriterTemplateMakerBuilder()
    
    def setupTemplateCandidateFor(self,candidateData):
        return self.__setupTemplateCandidateRecursively(self.__queueData.copy(),candidateData)
        
    def __setupTemplateCandidateRecursively(self,queueData,candidateData): 
        writerTemplateMaker = self.__builder.getWriterTemplateMakerFor(self.__getNext(queueData))
        writerTemplateMaker.select(candidateData)
        if writerTemplateMaker.isComplete() or self.__isQueueEmpty(queueData): 
            return writerTemplateMaker.getWriterTemplate()
        else: 
            return self.__setupTemplateCandidateRecursively(queueData,candidateData)       
    
    def __getNext(self,data):
        templateSpecificationData = data.pop(0)
        return TemplateSpec(templateSpecificationData)
    
    def __isQueueEmpty(self,queueData):
        return not bool(queueData)
    
class LanguageTemplateCollections(object):
    @staticmethod
    def getWithLanguageTag(languageTag):
        templateCollections = {'en':EnglishTemplateCollection(),
                               'nl':DutchTemplateCollection(),
                               'de':GermanTemplateCollection(),
                               'test':TestTemplateCollection()}
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
     'childrenListing':[{'template':"""$childDescription(main)"""}],                              
     'childDescription':[{'required':['main'],'template':"""$firstNameWithPIDAndGender"""+\
                          """(main)$baptismOnly(main)"""}],                              
     'nameWithPIDInText':[{'required':['main'],'template':"""(+foreNames)t.space(+lastName)"""+\
                           """t.firstLetterBold(+lastName)t.textPID(+PID)"""}],
     'firstNameWithPIDAndGender':[{'required':['main'],'template':"""(+foreNames)"""+\
                  """t.space()($boldGender(main))t.space()t.textPID(+PID)"""}],
      'boldGender':[{'required':['main'],'template':"""t.bold($gender(main))"""}],
      'gender':[{'required':['main'],'template':"""t.genderSymbol(+gender)"""}]}
    def __init__(self):
        self._dataDict = {**self._generalSpecifications,**self._languageSpecificSpecifications}
    
    def setupTemplateQueueWithName(self,name):
        return TemplateQueue(self._dataDict[name])  

class EnglishTemplateCollection(GeneralTemplateCollection):
    _languageSpecificSpecifications =\
    {'mainParagraph':[{'required':['main*','father','mother'],
                       'template':"""$nameWithPIDInText(main)"""+\
    """, son of $nameWithPIDInText(father) and $nameWithPIDInText(mother),$baptismOnly(main)"""},{'required':['main','father','mother'],
                       'template':"""$nameWithPIDInText(main) is a $child(main) of $nameWithPIDInText(father) and $nameWithPIDInText(mother)."""},
                      {'required':['main*'],'template':"""$nameWithPIDInText(main)$baptismOnly(main)"""}],
     'childListingIntro':[{'required':['father','mother','children'],'key':'children',
                           'modifier':'lengthOneOrMore',
               'map':{1:"""$FromARelationshipOfCouple(father,mother) was brought forth:""",
                      2:"""$FromARelationshipOfCouple(father,mother) were brought forth:"""}}],
     'FromARelationshipOfCouple':[{'required':['father','mother'],'template':"""From a relationship between $nameWithPIDInText(father) and $nameWithPIDInText(mother)"""}],
     'baptismOnly':[{'required':['main'],'template':""" was baptised $onTheDate(+date)"""+\
                     """$beforeTheChurches(main) at $town(main)$resp(+date)."""}],
     'resp':[{'required':['date'],'length':2,'template':""", respectively"""}],
     'onTheDate':[{'required':['date'],'length':2,'template':"""on the $dayOrdinal(+day) and 31\supscr{st} of $month(+month) (+year)"""},{'required':['date'],'template':"""on the $dayOrdinal(+day) of $month(+month) (+year)"""}],
     'dayOrdinal':[{'required':['day'],'template':"""(day)$dayOrdinalOnly(day)"""}],
     'dayOrdinalOnly':[{'modifier':'ordinalSelector','map':{0:'t.superScript(th)',1:'t.superScript(st)', 2:'t.superScript(th)'}}],
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

class TestTemplateCollection(EnglishTemplateCollection):
    __additionalTestSpecificSpecifications =\
    {'childDescriptionWithIntro':[{'template':"""$childListingIntro(main,spouse,children)"""+\
                                              """$childrenListing(children)"""}]}
    def __init__(self):
        self._dataDict = {**self._generalSpecifications,**self._languageSpecificSpecifications,
                          **self.__additionalTestSpecificSpecifications}   
    
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