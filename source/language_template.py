from source.template_maker import WriterTemplateMakerBuilder
from source.record_data import KeySpecification
        
class TemplateSpec(object):
    def __init__(self,templateDict):
        self.__dict = templateDict.copy()
        
    def getDict(self):
        return self.__dict
    
    def setTemplateTo(self,value):
        self.__dict['template'] = value
    
    def mapDataForCandidate(self,candidateData):
        candidateData = candidateData.getMainData()
        return self.mapData(candidateData.getData())
    
    def mapData(self,data):
        data = KeyModifiers.modifyData(self,data)
        return self.doMap(data)
    
    def doMap(self,key):
        return self.__dict['map'][key]
    
    def getKeyForMapping(self):
        return self.__dict['key']
    
    def getLength(self):
        return self.__dict['length']
    
    def getModifier(self):
        return self.__dict['modifier']
    
    def getRequiredKeys(self):
        return self.__dict['required'].copy()
    
    def getTemplate(self):
        return self.__dict['template']
    
    def hasNonTrivialLength(self):
        return 'length' in self.__dict
    
    def isKeyForMappingRequired(self):
        print('l.45 language_template.py refactoring')
        return self.getKeyForMapping() in self.getRequiredKeys()
    
    def isTemplateDefined(self):
        return 'template' in self.__dict
    
    def aModifierIsSpecified(self):
        return 'modifier' in self.__dict 
    
    def hasDataSelection(self):
        return 'required' in self.__dict
    
    def hasMappingDefined(self):
        return 'map' in self.__dict 
    
    def getWriterKeySpecifications(self):
        print('l.68 language_template.py refactoring')
        return KeySpecificationBuilder.buildFrom(self)       
    
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

$mainParagraph(main)$lineBreak(main)$childListingIntro(main,spouse,children)$childrenListing(children)$tmpSpouseParagraph(spouse)
"""}],
    'lineBreak':[{'required':['main','+date'],'template':"""\n\n"""}],
    'sectionHeader':[{'required':['main'],
                      'template':"""t.section($sectionTitle(main))t.label(+PID)"""}],
    'sectionTitle':[{'required':['main'],
                     'template':"""t.titlePID(+PID)t.nameInTitle(+foreNames,+lastName)"""+\
    """t.space()t.genderSymbol(+gender)"""}], 
     'childDescriptionWithIntro':[{'template':"""$childListingIntro(main,spouse,children)"""+\
                                               """$childrenListing(children)"""}],     
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
    {'mainParagraph':[{'required':['main','+father','+mother','+date'],
     'template':"""$nameWithPIDInText(main),"""+\
                """ $child(+gender)$parentRef(+father,+mother),$baptismOnly(main)"""}
                      ,{'required':['main','+father','+mother'],
     'template':"""$nameWithPIDInText(main) is a $child(+gender)$parentRef(+father,+mother)."""},
                      {'required':['main','+date'], 'template':"""$nameWithPIDInText(main)$baptismOnly(main)"""}],
     'childListingIntro':[{'required':['father','mother','children'],'key':'children',
                           'modifier':'lengthOneOrMore',
               'map':{1:"""$FromARelationshipOfCouple(father,mother) was brought forth:""",
                      2:"""$FromARelationshipOfCouple(father,mother) were brought forth:"""}}],
     'FromARelationshipOfCouple':[{'required':['father','mother'],'template':"""From a relationship between $nameWithPIDInText(father) and $nameWithPIDInText(mother)"""}],
     'baptismOnly':[{'required':['main','+town'],'template':""" was baptised $onTheDate(+date)"""+\
                     """$beforeTheChurches(main) at (+town)$resp(+date)."""}],
     'resp':[{'required':['date'],'length':2,'template':""", respectively"""}],
     'onTheDate':[{'required':['date'],'length':2,'template':"""on the $dayOrdinal(+day) and 31\supscr{st} of $month(+month) (+year)"""},{'required':['date'],'template':"""on the $dayOrdinal(+day) of $month(+month) (+year)"""}],
     'dayOrdinal':[{'required':['day'],'template':"""(day)$dayOrdinalOnly(day)"""}],
     'dayOrdinalOnly':[{'modifier':'ordinalSelector','map':{0:'t.superScript(th)',1:'t.superScript(st)', 2:'t.superScript(th)'}}],
     'month':[{'modifier':'toInt','map':{0:'',1:'January',2:'February',4:'April',5:'May',
                                         6:'June',7:'July',8:'August',9:'September',
                                         11:'November',12:'December'}}],
     'child':[{'map':{'m':'son','f':'daughter','':'child'}}],
      'parentRef':[{'required':['father','mother'],'template':""" of $nameWithPIDInText(father) and $nameWithPIDInText(mother)"""}],
     'beforeTheChurches':[{'required':['main'],'key':'denom','modifier':'primalListSelector',
                           'map':{'rc':""" before the catholic church$ofTheNamedParish(main)$andChurchBoth(main)""",'ref':""" before the reformed church$ofTheNamedParish(main)$andChurchBoth(main)""",'':''}}],
     'ofTheNamedParish':[{'required':['main','+nameOfParish'],'key':'denom',
                          'modifier':'primalListSelector',
                          'map':{'rc':' of the t.italic(+nameOfParish) parish','ref':'','':''}}],
     'andChurchBoth':[{'required':['main'],'key':'denom','modifier':'secondaryListSelector',
                       'map':{'ref':' and the reformed church, both','rc':'','':''}}],
    'tmpSpouseParagraph':[{'required':['main','+date'],'template':"""\nHis spouse $nameWithPIDInText(main), $child(+gender)$parentRef(+father,+mother),$baptismOnly(main)"""}]}

class TestTemplateCollection(EnglishTemplateCollection):
    __additionalTestSpecificSpecifications = {}
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
    def modifyData(templateSpec,data):
        if templateSpec.aModifierIsSpecified():
            modifierName = templateSpec.getModifier()
            return KeyModifiers.__doModifyData(modifierName,data)
        else: return data
    
    @staticmethod
    def __doModifyData(modifierName,data):
        method = getattr(KeyModifiers(),modifierName)()
        return method(data)
        
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