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
        if   key == 'child': return self._child[value]
        elif key == 'month': return self._months[int(value)]
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
    pass

class DutchSentences(Sentences):    
    _sentences = {'baptismOnly':'$usedName is gedoopt $onTheDate$beforeChurches te $town.',
                  'childListingIntro':'$FromARelationshipOfCouple is voortgebracht:',
                  'childrenListingIntro':'$FromARelationshipOfCouple zijn voortgebracht:'}
    _clauses   = {'FromARelationshipOfCouple':'Uit een relatie tussen $nameOfMainParent en $nameOfOtherParent',
                  'ofTheNamedParish':' van de $nameOfParish_it parochie',
                  'beforeTheChurches':' voor de $denom_0 kerk$ofTheNamedParish$andChurchBoth',
                  'andChurchBoth':' en de $denom_1 kerk, beide'}
    _denoms    = {'rc':'katholieke','ref':'gereformeerde'}

class GermanSentences(Sentences):   
    _sentences = {'baptismOnly':'$usedName ist $onTheDate getauft$beforeChurches zu $town.',
                  'childListingIntro':'$FromARelationshipOfCouple ist geboren worden:',
                  'childrenListingIntro':'$FromARelationshipOfCouple sind geboren worden:'}
    _clauses   = {'FromARelationshipOfCouple':'From a relationship between $nameOfMainParent and $nameOfOtherParent',
                  'ofTheNamedParish':' der $nameOfParish_it Pfarrei',
                  'beforeTheChurches':' vor der $denom_0 Kirche$ofTheNamedParish$andChurchBoth',
                  'andChurchBoth':' und der $denom_1 Kirche, beiden'}
    _denoms    = {'rc':'katholischen','ref':'reformierten'}  
