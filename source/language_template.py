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
     'nameWithPIDInText':[{'required':['main'],
                       'template':"""(+foreNames) t.firstLetterBold(+lastName)t.textPID(+PID)"""}]}
    
    def getTemplateCollectionWithName(self,name):
        specifications = {**self._generalSpecifications,**self._languageSpecificSpecifications}
        return specifications[name].copy()
        

class EnglishTemplateCollection(GeneralTemplateCollection):
    _languageSpecificSpecifications =\
    {'mainParagraph':[{'required':['main*','father','mother'],
                       'template':"""$nameWithPIDInText(main)"""+\
    """, son of $nameWithPIDInText(father) and $nameWithPIDInText(mother),"""},
                      {'required':['main','father','mother'],
                       'template':"""$nameWithPIDInText(main) is a $child(main)"""},
                      {'required':['main*'],'template':"""$nameWithPIDInText(main)"""}],
     'child':[{'required':['main'],'key':'gender','map':{'m':'son','':'child'}}]}

class DutchTemplateCollection(GeneralTemplateCollection):
    _languageSpecificSpecifications =\
    {'mainParagraph':[{'required':['main*','father','mother'],
                       'template':"""$nameWithPIDInText(main)"""+\
    """, zoon van $nameWithPIDInText(father) en $nameWithPIDInText(mother),"""},
                         {'required':['main*'],'template':"""$nameWithPIDInText(main)"""}]}

class GermanTemplateCollection(GeneralTemplateCollection):
    _languageSpecificSpecifications =\
    {'mainParagraph':[{'required':['main*','father','mother'],
                          'template':"""$nameWithPIDInText(main)"""+\
    """, Sohn von $nameWithPIDInText(father) und $nameWithPIDInText(mother),"""},
                         {'required':['main*'],'template':"""$nameWithPIDInText(main)"""}]}