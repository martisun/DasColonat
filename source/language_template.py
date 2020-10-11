class LanguageTemplateSelector(object):
    @staticmethod
    def getTemplateCollectionInLanguage(languageTag):
        templateCollections = {'en':EnglishTemplateCollection(),
                               'nl':DutchTemplateCollection(),
                               'de':GermanTemplateCollection()}
        return templateCollections[languageTag]  

class GeneralTemplateCollection(object):
    _generalSpecifications = {'summary':[{'template':"""
$sectionHeader(main)

$mainParagraph(main,father,mother)"""}],    
    'sectionHeader':[{'required':['main'],
                      'template':"""t.section($sectionTitle(main))t.label(+PID)"""}],
    'sectionTitle':[{'required':['main'],
                     'template':"""t.titlePID(+PID)t.nameInTitle(+foreNames,+lastName)"""+\
    """t.space()t.genderSymbol(+gender)"""}],
     'childDescription':[{'required':['main'],'template':"""$firstNameWithPIDAndGender"""+\
                          """(main)$baptismOnly(main)"""}],
     'nameWithPIDInText':[{'required':['main'],'template':"""(+foreNames)t.space(+lastName)"""+\
                           """t.firstLetterBold(+lastName)t.textPID(+PID)"""}],
     'firstNameWithPIDAndGender':[{'required':['main'],'template':"""(+foreNames)"""+\
                  """t.space()($boldGender(main))t.space()t.textPID(+PID)"""}],
      'boldGender':[{'required':['main'],'template':"""t.bold($gender(main))"""}],
      'gender':[{'required':['main'],'template':"""t.genderSymbol(+gender)"""}]}
    @staticmethod
    def ordinalSelector():
        getLastDigit = lambda x: int(x)%10
        selectFirst  = lambda x: min(2,getLastDigit(x))
        return selectFirst
    
    @staticmethod
    def primalListSelector():
        return GeneralTemplateCollection.__listSelector(0)
    
    @staticmethod
    def secondaryListSelector():
        return GeneralTemplateCollection.__listSelector(1)
    
    def initialize(self,templateDict):
        if 'modifier' in templateDict:
            method = self.__getPrivateMethodNamed(templateDict['modifier'])
            return {**templateDict,'modifier':method()}
        else: return templateDict
    
    def getTemplateCollectionWithName(self,name):
        specifications = {**self._generalSpecifications,**self._languageSpecificSpecifications}
        return specifications[name].copy()
    
    def __getPrivateMethodNamed(self,nameOfMethod):
        return getattr(self,nameOfMethod)
    
    def __listSelector(index):
        def listSelector(x):
            if index < len(x): return x[index]
            else:              return ''
        return listSelector        

class EnglishTemplateCollection(GeneralTemplateCollection):
    _languageSpecificSpecifications =\
    {'mainParagraph':[{'required':['main*','father','mother'],
                       'template':"""$nameWithPIDInText(main)"""+\
    """, son of $nameWithPIDInText(father) and $nameWithPIDInText(mother),$baptismOnly(main)"""},
                      {'required':['main','father','mother'],
                       'template':"""$nameWithPIDInText(main) is a $child(main) of $nameWithPIDInText(father) and $nameWithPIDInText(mother)."""},
                      {'required':['main*'],'template':"""$nameWithPIDInText(main)$baptismOnly(main)"""}],
     'FromARelationshipOfCouple':[{'required':['father','mother'],'template':"""From a relationship between $nameWithPIDInText(father) and $nameWithPIDInText(mother)"""}],
     'childListingIntro':[{'required':['father','mother'],
               'template':"""$FromARelationshipOfCouple(father,mother) was brought forth:"""}],
     'childrenListingIntro':[{'required':['father','mother'],
               'template':"""$FromARelationshipOfCouple(father,mother) were brought forth:"""}],
     'baptismOnly':[{'required':['main'],'template':""" was baptised $onTheDate(main)"""+\
                     """$beforeTheChurches(main) at $town(main)."""}],
     'onTheDate':[{'required':['main'],
                   'template':"""on the $dayOrdinal(main) of $month(main) (+year)"""}],
     'dayOrdinal':[{'required':['main'],'key':'day','modifier':'ordinalSelector',
                    'map':{1:'$dayst(main)',2:'$dayth(main)'}}],
     'dayth':[{'required':['main'],'template':"""(+day)t.superScript(th)"""}],
     'dayst':[{'required':['main'],'template':"""(+day)t.superScript(st)"""}],
     'month':[{'required':['main'],'key':'month',
               'map':{2:'February',5:'May',6:'June',7:'July',12:'December'}}],
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