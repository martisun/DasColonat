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
        relationshipClause = self.__compileRelationshipClause(mainParent,otherParent)
        return self.__fillOutRelationshipClauseIntoSentenceWithTag(relationshipClause,
                                                                   'childListingIntro')
    
    def childrenListingIntroForParents(self,mainParent,otherParent):        
        relationshipClause = self.__compileRelationshipClause(mainParent,otherParent)
        return self.__fillOutRelationshipClauseIntoSentenceWithTag(relationshipClause,
                                                                   'childrenListingIntro')
    
    def mainDescription(self,main,father,mother):
        return self.__compileBaptismOnlyConcerning('',main)
    
    def __fillOutRelationshipClauseIntoSentenceWithTag(self,relationshipClause,sentenceTag):
        inputData = {'FromARelationshipOfCouple':relationshipClause}
        self.__sentences.selectSentenceWithTag(sentenceTag)
        return self.__sentences.fillOutBlanksWith(inputData)
    
    def replaceSpecialCharacters(self,text):
        return self.__templater.replaceSpecialCharacters(text)

    def __compileChildDescriptionInListingOf(self,child):  
        childName      = self.__compileFirstNameWithPIDAndGenderOf(child)
        return self.__compileBaptismOnlyConcerning(childName,child)
        
    def __compileBaptismOnlyConcerning(self,usedName,person):    
        dateOfBaptism  = self.__compileDateOfEvent(person) 
        placeOfBaptism = self.__compilePlaceOfEvent(person)
        inputData ={'usedName':usedName,'onTheDate':dateOfBaptism,
                    'beforeChurches':placeOfBaptism,'town': 'Freren'}
        self.__sentences.selectSentenceWithTag('baptismOnly')
        return self.__sentences.fillOutBlanksWith(inputData)    
    
    def __compileDateOfEvent(self,person):
        dateWriter = self.__writerMaker.parse('$onTheDate(main)')[0]
        return dateWriter.write({'main':person})
    
    def __compileFirstNameWithPIDAndGenderOf(self,person):
        nameWriter = self.__writerMaker.parse('$firstNameWithPIDAndGenderInText(main)')[0]
        return nameWriter.write({'main':person})
    
    def __compileNameWithPIDInTextOf(self,person):
        nameWriter = self.__writerMaker.parse('$nameWithPIDInText(main)')[0]
        return nameWriter.write({'main':person})
    
    def __compileParishName(self,child):
        parishNameWriter = self.__writerMaker.parse('$ofTheNamedParish(main)')[0]
        return parishNameWriter.write({'main':child})
    
    def __compilePlaceOfEvent(self,child):
        parishName = self.__compileParishName(child)
        inputData = {'denom_0':child.get('denom'),'ofTheNamedParish':parishName,
                     'andChurchBoth':''}
        if len([elem for elem in inputData['denom_0'] if elem != '']) > 1:
            additionalChurchReference = self.__compileAdditionalChurch(child)
            inputData = {**inputData,'andChurchBoth':additionalChurchReference}
        self.__sentences.selectClauseWithTag('beforeTheChurches')
        return self.__sentences.fillOutBlanksWith(inputData)        
    
    def __compileAdditionalChurch(self,child):
        self.__sentences.selectClauseWithTag('andChurchBoth')
        return self.__sentences.fillBlanksWith(child)
        
    def __compileRelationshipClause(self,mainParent,otherParent):
        nameOfMainParent  = self.__compileNameWithPIDInTextOf(mainParent)
        nameOfOtherParent = self.__compileNameWithPIDInTextOf(otherParent) 
        inputData = {'nameOfMainParent':nameOfMainParent,
                     'nameOfOtherParent':nameOfOtherParent}
        self.__sentences.selectClauseWithTag('FromARelationshipOfCouple')
        return self.__sentences.fillOutBlanksWith(inputData)

        