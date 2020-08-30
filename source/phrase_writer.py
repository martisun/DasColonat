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
    
    def addChildListing(self):
        self.__sentences.selectSentenceWithTag('childReference')
        inputData ={'child':'Wolterus~(\textbf{?})~\pids{(Fr0.1)}',
                    'day_th': '18','year':'1661',
                    'nameOfParish_it': 'St. Vitus','town': 'Freren'}
        addChildren = self.__sentences.fillOutBlanksWith(inputData)
        return self.__templater.compileListingOf(addChildren)
    
    def childListingIntroForParents(self,mainParent,otherParent):
        self.__sentences.selectSentenceWithTag('childListingIntro')
        nameOfMainParent  = self.__compileNameWithPIDInTextOf(mainParent)
        nameOfOtherParent = self.__compileNameWithPIDInTextOf(otherParent) 
        inputData = {'nameOfMainParent':nameOfMainParent,
                     'nameOfOtherParent':nameOfOtherParent}
        return self.__sentences.fillOutBlanksWith(inputData)
    
    def sectionHeader(self,person):
        section = self.__compileSection(person)
        label   = self.__compileLabel(person)
        return section+label
    
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
        genderSymbol = person.get('gender')
        return self.__templater.genderSymbol(genderSymbol)
    
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
        