from source.latex_templater import LatexTemplater
from source.sentence_templates import SentenceSelector

class PhraseWriter(object):    
    @staticmethod
    def inLanguage(languageTag):
        sentences = SentenceSelector.getSentencesInLanguage(languageTag)  
        phraseWriter = PhraseWriter(sentences)
        return phraseWriter
    
    def __init__(self,sentences):
        self.__sentences = sentences
        self.__templater = LatexTemplater()       
    
    def setWriterMakerTo(self,writerMaker):
        self.__writerMaker = writerMaker
    
    def childrenDescriptionsInListing(self,children):
        childrenListing = [self.__compileChildDescriptionInListingOf(child) for child in children]
        return self.__templater.compileListingOf(childrenListing)
    
    def childListingIntroForParents(self,mainParent,otherParent):        
        childListingIntroWriter =\
                  self.__writerMaker.parse('$childListingIntro(father,mother)')[0]
        return childListingIntroWriter.write({'father':mainParent,'mother':otherParent})
    
    def childrenListingIntroForParents(self,mainParent,otherParent): 
        childrenListingIntroWriter =\
                  self.__writerMaker.parse('$childrenListingIntro(father,mother)')[0]
        return childrenListingIntroWriter.write({'father':mainParent,'mother':otherParent})
    
    def replaceSpecialCharacters(self,text):
        return self.__templater.replaceSpecialCharacters(text)

    def __compileChildDescriptionInListingOf(self,child):  
        childDescriptionWriter = self.__writerMaker.parse('$childDescription(main)')[0]
        return childDescriptionWriter.write({'main':child})  

        