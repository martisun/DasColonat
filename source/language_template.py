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
        if   self.__isPostFixInString('th',key): value  = self._getOrdinalOf(value)
        elif self.__isPostFixInString('it',key): value  = self._templater.italic(value) 
        return value 
    
    @staticmethod
    def __isPostFixInString(postFix,string):
        return string.endswith('_%s'%postFix)
    
    def __substituteBlanksWith(self,inputData):
        return Template(self._form).substitute(inputData)
    
    def __translateValueForKey(self,value,key):
        if key == 'month': return self._months[int(value)]
        else:              return value
    
class EnglishSentences(Sentences):    
    _sentences = {'childReference':'$child was baptised $onTheDate before the catholic church of the $nameOfParish_it parish at $town.',
                  'childListingIntro':'From a relationship between $nameOfMainParent and $nameOfOtherParent was brought forth:'}
    _clauses   = {'onTheDate':'on the $day_th of $month $year'}
    _months    = {6:'June',12:'December'}
    
    def _getOrdinalOf(self,value):
        if int(value) == 1: ordinal = 'st'
        else:               ordinal = 'th'
        return str(value)+self._templater.superScript(ordinal)

class DutchSentences(Sentences):    
    _sentences = {'childReference':'$child is gedoopt $onTheDate voor de katholieke kerk van de $nameOfParish_it parochie te $town.',
                  'childListingIntro':'Uit een relatie tussen $nameOfMainParent en $nameOfOtherParent is voortgebracht:'}
    _clauses   = {'onTheDate':'op de $day_th $month $year'}
    _months    = {6:'juni',12:'december'}
    
    def _getOrdinalOf(self,value):
        if int(value) == 1: ordinal = 'ste'
        else:               ordinal = 'de'
        return str(value)+self._templater.superScript(ordinal)

class GermanSentences(Sentences):   
    _sentences = {'childReference':'$child ist $onTheDate getauft vor dem katholischen Kirche der $nameOfParish_it Pfarrei zu $town.',
                  'childListingIntro':'Aus einer Beziehung zwischen $nameOfMainParent und $nameOfOtherParent ist geboren worden:'}
    _clauses   = {'onTheDate':'am $day_th $month $year'}
    _months    = {6:'Juni',12:'Dezember'}
    
    def _getOrdinalOf(self,value):
        return str(value)+'.'
