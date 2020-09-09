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
    
    def childrenListingIntroForParents(self,mainParent,otherParent):
        nameOfMainParent  = self.__compileNameWithPIDInTextOf(mainParent)
        nameOfOtherParent = self.__compileNameWithPIDInTextOf(otherParent) 
        inputData = {'nameOfMainParent':nameOfMainParent,
                     'nameOfOtherParent':nameOfOtherParent}
        self.__sentences.selectSentenceWithTag('childListingIntro')
        return self.__sentences.fillOutBlanksWith(inputData)
    
    def replaceSpecialCharacters(self,text):
        return self.__templater.replaceSpecialCharacters(text)
    
    def sectionHeader(self,person):
        section = self.__compileSection(person)
        label   = self.__compileLabel(person)
        return section+label

    def __compileChildDescriptionInListingOf(self,child):        
        childName     = self.__compileFirstNameWithPIDAndGenderOf(child)
        dateOfBaptism = self.__compileDateOfEvent(child) 
        inputData ={'child':childName,'onTheDate':dateOfBaptism,
                    'nameOfParish_it': 'St. Vitus','town': 'Freren'}
        self.__sentences.selectSentenceWithTag('childReference')
        return self.__sentences.fillOutBlanksWith(inputData)    
    
    def __compileDateOfEvent(self,person):
        inputData = {'day_th':person.get('day'),
                     'month':person.get('month'),
                     'year':person.get('year') }
        self.__sentences.selectClauseWithTag('onTheDate')
        return self.__sentences.fillOutBlanksWith(inputData)
    
    def __compileFirstNameWithPIDAndGenderOf(self,person):
        firstName   = person.get('firstName')
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
    
    def __compileNameWithPIDInTextOf(self,person):
        firstName = person.get('firstName')
        lastName  = self.__compileLastNameInTextOf(person) 
        PIDinText = self.__templater.textPID(person.get('PID'))
        return firstName+lastName+PIDinText
    
    def __compileLastNameInTextOf(self,person):
        lastName = person.get('lastName')
        if lastName != '': lastName = ' %s'%self.__templater.firstLetterBold(lastName)
        return lastName 
    
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
        firstName = person.get('firstName')
        lastName  = person.get('lastName')
        return self.__templater.nameInTitle(firstName,lastName)
    
    def __compilePIDInTitle(self,person):
        pidOfMainParent = person.get('PID')
        return self.__templater.titlePID(pidOfMainParent)
    
    def __compileLabel(self,person):
        pidOfPerson = person.get('PID')
        return self.__templater.label(pidOfPerson)
        