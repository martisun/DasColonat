import re
from string import Template

from source.latex_templater import LatexTemplater
        
class SentenceSelector(object):
    @staticmethod
    def getSentencesInLanguage(languageTag):
        sentenceCollections = {'en':EnglishSentences(),
                               'nl':DutchSentences(),
                               'de':GermanSentences()}
        return sentenceCollections[languageTag]    

class Sentences(object):
    def __init__(self):
        self._templater = LatexTemplater() 
    
    def selectSentenceWithTag(self,sentenceTag):
        self._form = self._sentences[sentenceTag]
        
    def selectClauseWithTag(self,clauseTag):
        self._form = self._clauses[clauseTag]
    
    def fillBlanksWith(self,person):
        requestedKeys = self.__extractKeysFromForm()
        inputData = {key:self.__extractValueFromDataWithKey(person,key) for key in requestedKeys}
        return self.fillOutBlanksWith(inputData)
    
    def fillOutBlanksWith(self,inputData):
        inputData = self.__formatInputData(inputData)
        return self.__substituteBlanksWith(inputData)    
    
    def __formatInputData(self,inputData):
        return {key:self.__formatValueForKey(inputData[key],key) for key in inputData}
    
    def __formatValueForKey(self,value,key):
        value = self.__formatValueForPostFixes(value,key)
        value = self.__translateValueForKey(value,key) 
        return value
    
    def __formatValueForPostFixes(self,value,key):
        postFix = self.__extractPostFix(key)
        if not postFix is None:
            if postFix   == 'th':    value  = self._getOrdinalOf(value)
            elif postFix == 'it':    value  = self._templater.italic(value)
            elif postFix.isnumeric(): value = value[int(postFix)]   
        return value 
    
    @staticmethod
    def __extractPostFix(string):
        postFixCandidates = re.findall('_(\d+|\w+)$',string)
        if postFixCandidates: return postFixCandidates[0]
    
    def __substituteBlanksWith(self,inputData):
        return Template(self._form).substitute(inputData)
    
    def __translateValueForKey(self,value,key):
        key   = self.__removePostFix(key)
        if key == 'month':   return self._months[int(value)]
        elif key == 'denom': return self._denoms[value]
        else:                return value
    
    def __extractKeysFromForm(self):
        return re.findall('\$(\w+)',self._form)
    
    @staticmethod
    def __extractValueFromDataWithKey(data,key):
        keyWithoutFormatting = Sentences.__removePostFix(key)
        return data.get(keyWithoutFormatting)
    
    @staticmethod
    def __removePostFix(key):
        return re.sub('\_\w+$', '', key)
    
class EnglishSentences(Sentences):    
    _sentences = {'childReference':'$child was baptised $onTheDate$beforeChurches at $town.',
                  'childListingIntro':'$FromARelationshipOfCouple was brought forth:',
                  'childrenListingIntro':'$FromARelationshipOfCouple were brought forth:'}
    _clauses   = {'FromARelationshipOfCouple':'From a relationship between $nameOfMainParent and $nameOfOtherParent',
                  'onTheDate':'on the $day_th of $month $year',
                  'ofTheNamedParish':' of the $nameOfParish_it parish',
                  'beforeTheChurches':' before the $denom_0 church$ofTheNamedParish$andChurchBoth',
                  'andChurchBoth':' and the $denom_1 church, both'}
    _months    = {2:'February',5:'May',6:'June',7:'July',12:'December'}
    _denoms    = {'rc':'catholic','ref':'reformed'}
    
    def _getOrdinalOf(self,value):
        if int(value)%10 == 1: ordinal = 'st'
        else:                  ordinal = 'th'
        return str(value)+self._templater.superScript(ordinal)

class DutchSentences(Sentences):    
    _sentences = {'childReference':'$child is gedoopt $onTheDate$beforeChurches te $town.',
                  'childListingIntro':'$FromARelationshipOfCouple is voortgebracht:',
                  'childrenListingIntro':'$FromARelationshipOfCouple zijn voortgebracht:'}
    _clauses   = {'FromARelationshipOfCouple':'Uit een relatie tussen $nameOfMainParent en $nameOfOtherParent',
                  'onTheDate':'op de $day_th $month $year',
                  'ofTheNamedParish':' van de $nameOfParish_it parochie',
                  'beforeTheChurches':' voor de $denom_0 kerk$ofTheNamedParish$andChurchBoth',
                  'andChurchBoth':' en de $denom_1 kerk, beide'}
    _months    = {2:'februari',5:'mei',6:'juni',7:'juli',12:'december'}
    _denoms    = {'rc':'katholieke','ref':'gereformeerde'}
    
    def _getOrdinalOf(self,value):
        if int(value)%10 == 1: ordinal = 'ste'
        else:                  ordinal = 'de'
        return str(value)+self._templater.superScript(ordinal)

class GermanSentences(Sentences):   
    _sentences = {'childReference':'$child ist $onTheDate getauft$beforeChurches zu $town.',
                  'childListingIntro':'$FromARelationshipOfCouple ist geboren worden:',
                  'childrenListingIntro':'$FromARelationshipOfCouple sind geboren worden:'}
    _clauses   = {'FromARelationshipOfCouple':'From a relationship between $nameOfMainParent and $nameOfOtherParent',
                  'onTheDate':'am $day_th $month $year',
                  'ofTheNamedParish':' der $nameOfParish_it Pfarrei',
                  'beforeTheChurches':' vor der $denom_0 Kirche$ofTheNamedParish$andChurchBoth',
                  'andChurchBoth':' und der $denom_1 Kirche, beiden'}
    _months    = {2:'Februar',5:'Mai',6:'Juni',7:'Juli',12:'Dezember'}
    _denoms    = {'rc':'katholischen','ref':'reformierten'}
    
    def _getOrdinalOf(self,value):
        return str(value)+'.'
