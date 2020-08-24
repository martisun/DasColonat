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
        
    def setMainParentTo(self,mainParent):
        self.__mainParent = mainParent
        
    def setOtherParentTo(self,otherParent):
        self.__otherParent = otherParent        
    
    def addChildListing(self):
        self.__sentences.selectSentenceWithTag('childReference')
        inputData ={'child':'Wolterus~(\textbf{?})~\pids{(Fr0.1)}',
                    'day_th': '18','year':'1661',
                    'nameOfParish_it': 'St. Vitus','town': 'Freren'}
        addChildren = self.__sentences.fillOutBlanksWith(inputData)
        return self.__templater.compileListingOf(addChildren)
    
    def childListingIntro(self):
        self.__sentences.selectSentenceWithTag('childListingIntro')
        nameOfMainParent  = self.__compileNameWithPIDInTextOf(self.__mainParent)
        nameOfOtherParent = self.__compileNameWithPIDInTextOf(self.__otherParent) 
        inputData = {'nameOfMainParent':nameOfMainParent,
                     'nameOfOtherParent':nameOfOtherParent}
        return self.__sentences.fillOutBlanksWith(inputData)
    
    def sectionHeader(self):
        section = self.__compileSection()
        label   = self.__compileLabel()
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
    
    def __compileSection(self):
        title = self.__compileTitle()
        return self.__templater.section(title)
    
    def __compileTitle(self):
        pidInTitle   = self.__compilePIDInTitle()
        nameInTitle  = self.__compileNameInTitle()
        genderSymbol = self.__compileGenderSymbolInTitle()
        return pidInTitle+nameInTitle+genderSymbol

    def __compileGenderSymbolInTitle(self):
        genderSymbol = self.__mainParent.get('gender')
        return self.__templater.genderSymbol(genderSymbol)
    
    def __compileNameInTitle(self):
        firstName = self.__mainParent.get('firstName')
        lastName  = self.__mainParent.get('lastName')
        return self.__templater.nameInTitle(firstName,lastName)
    
    def __compilePIDInTitle(self):
        pidOfMainParent = self.__mainParent.get('PID')
        return self.__templater.titlePID(pidOfMainParent)
    
    def __compileLabel(self):
        pidOfMainParent = self.__mainParent.get('PID')
        return self.__templater.label(pidOfMainParent)
        