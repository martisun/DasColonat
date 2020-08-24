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
        self._sentence = self._sentences[sentenceTag]    
    
    def fillOutBlanksWith(self,inputData):
        inputData = self.__formatInputData(inputData)
        return self.__substituteBlanksWith(inputData)    
    
    def __formatInputData(self,inputData):
        return {key:self.__formatValueForKey(inputData[key],key) for key in inputData}
    
    def __formatValueForKey(self,value,key):
        if   self.__isPostFixInString('th',key): value += self._getOrdinal()
        elif self.__isPostFixInString('it',key): value  = self._templater.italic(value) 
        return value
    
    @staticmethod
    def __isPostFixInString(postFix,string):
        return string.endswith('_%s'%postFix)
    
    def __substituteBlanksWith(self,inputData):
        return Template(self._sentence).substitute(inputData)
    
class EnglishSentences(Sentences):    
    _sentences = {'childReference':'$child was baptised on the $day_th of December $year before the catholic church of the $nameOfParish_it parish at $town.',
                  'childListingIntro':'From a relationship between $nameOfMainParent and $nameOfOtherParent was brought forth:'}
    
    def _getOrdinal(self):
        return self._templater.superScript('th')

class DutchSentences(Sentences):    
    _sentences = {'childReference':'$child is gedoopt op de $day_th december $year voor de katholieke kerk van de $nameOfParish_it parochie te $town.',
                  'childListingIntro':'Uit een relatie tussen $nameOfMainParent en $nameOfOtherParent is voortgebracht:'}
    
    def _getOrdinal(self):
        return self._templater.superScript('de')

class GermanSentences(Sentences):   
    _sentences = {'childReference':'$child ist am $day_th Dezember $year getauft vor dem katholischen Kirche der $nameOfParish_it Pfarrei zu $town.',
                  'childListingIntro':'Aus einer Beziehung zwischen $nameOfMainParent und $nameOfOtherParent ist geboren worden:'}
    
    def _getOrdinal(self):
        return '.'
