from source.latex_templater import LatexTemplater
from source.language_template import SentenceSelector

class PhraseWriter(object):    
    @staticmethod
    def inLanguage(languageTag):
        sentences = SentenceSelector.getSentencesInLanguage(languageTag)  
        phraseWriter = PhraseWriter(sentences)
        return phraseWriter
    
    def __init__(self,sentences):
        self.__sentences = sentences
        self.__templater = LatexTemplater()       
    
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
        mainNameWithParents = self.__compileMainNameWithParentsClause(main,father,mother)
        return self.__compileBaptismOnlyConcerning(mainNameWithParents,main)
    
    def __fillOutRelationshipClauseIntoSentenceWithTag(self,relationshipClause,sentenceTag):
        inputData = {'FromARelationshipOfCouple':relationshipClause}
        self.__sentences.selectSentenceWithTag(sentenceTag)
        return self.__sentences.fillOutBlanksWith(inputData)
    
    def parentReference(self,main,father,mother):
        nameOfMain       = self.__compileNameWithPIDInTextOf(main)
        nameOfFather     = self.__compileNameWithPIDInTextOf(father)
        nameOfMother     = self.__compileNameWithPIDInTextOf(mother)
        inputData = {'nameOfMain':nameOfMain,'child':main.get('gender'),
                     'nameOfFather':nameOfFather,'nameOfMother':nameOfMother}
        self.__sentences.selectSentenceWithTag('MainNameWithParents')
        return self.__sentences.fillOutBlanksWith(inputData) 
    
    def replaceSpecialCharacters(self,text):
        return self.__templater.replaceSpecialCharacters(text)
    
    def sectionHeader(self,person):
        section = self.__compileSection(person)
        label   = self.__compileLabel(person)
        return section+label

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
        self.__sentences.selectClauseWithTag('onTheDate')
        return self.__sentences.fillBlanksWith(person)
    
    def __compileFirstNameWithPIDAndGenderOf(self,person):
        firstName   = person.get('foreNames')
        PIDinText   = self.__templater.textPID(person.get('PID'))
        genderSymbolInText = self.__compileGenderSymbolInText(person)
        spaceInText = self.__templater.space() 
        return firstName+genderSymbolInText+spaceInText+PIDinText
    
    def __compileGenderSymbolInText(self,person):
        spaceInText  = self.__templater.space() 
        genderSymbol = person.get('gender')
        genderSymbolInText     = self.__templater.genderSymbol(genderSymbol)
        boldGenderSymbolInText = self.__templater.bold(genderSymbolInText)
        return spaceInText+'(%s)'%boldGenderSymbolInText
    
    def __compileMainNameWithParentsClause(self,main,father,mother):
        nameOfMain       = self.__compileNameWithPIDInTextOf(main)
        nameOfFather     = self.__compileNameWithPIDInTextOf(father)
        nameOfMother     = self.__compileNameWithPIDInTextOf(mother)
        inputData = {'nameOfMain':nameOfMain,'child':main.get('gender'),
                     'nameOfFather':nameOfFather,'nameOfMother':nameOfMother}
        self.__sentences.selectClauseWithTag('MainNameWithParents')
        return self.__sentences.fillOutBlanksWith(inputData) 
    
    def __compileNameWithPIDInTextOf(self,person):
        firstName = person.get('foreNames')
        lastName  = self.__compileLastNameInTextOf(person) 
        PIDinText = self.__templater.textPID(person.get('PID'))
        return firstName+lastName+PIDinText
    
    def __compileLastNameInTextOf(self,person):
        lastName = person.get('lastName')
        if lastName != '': lastName = ' %s'%self.__templater.firstLetterBold(lastName)
        return lastName 
    
    def __compileParishName(self,child):
        if child.get('denom')[0] == 'rc':
            self.__sentences.selectClauseWithTag('ofTheNamedParish')
            return self.__sentences.fillBlanksWith(child)
        else: return ''
    
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
    
    def __compileSection(self,person):
        title = self.__compileTitle(person)
        return self.__templater.section(title)
    
    def __compileTitle(self,person):
        pidInTitle   = self.__compilePIDInTitle(person)
        nameInTitle  = self.__compileNameInTitle(person) 
        genderSymbol = self.__compileGenderSymbolInTitle(person)
        return pidInTitle+nameInTitle+genderSymbol

    def __compileGenderSymbolInTitle(self,person):
        spaceInText  = self.__templater.space()
        genderSymbol = person.get('gender')
        return spaceInText+self.__templater.genderSymbol(genderSymbol)
    
    def __compileNameInTitle(self,person):
        firstName = person.get('foreNames')
        lastName  = person.get('lastName')
        return self.__templater.nameInTitle(firstName,lastName)
    
    def __compilePIDInTitle(self,person):
        pidOfMainParent = person.get('PID')
        return self.__templater.titlePID(pidOfMainParent)
    
    def __compileLabel(self,person):
        pidOfPerson = person.get('PID')
        return self.__templater.label(pidOfPerson)
        