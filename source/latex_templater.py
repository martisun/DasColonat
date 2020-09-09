class LatexTemplater(object):
    @staticmethod
    def bold(text):
        return '\textbf{%s}'%text
    
    @staticmethod
    def compileListingOf(items):
        prefixedItems = LatexTemplater.__itemsWithPrefix(items)
        joinedItems   = '\n'.join(prefixedItems)
        return '\begin{itemize}\n%s\n\end{itemize}'%joinedItems
    
    @staticmethod
    def firstLetterBold(text):
        firstLetter = LatexTemplater.bold(text[0])
        remainder   = text[1:]
        return firstLetter+remainder
    
    @staticmethod
    def genderSymbol(genderIndicator):
        genderSymbols = {'m':'\Mars','v':'\Venus','':'?'}
        return genderSymbols[genderIndicator]
    
    @staticmethod
    def italic(name):
        return '{\it %s}'%name
    
    @staticmethod
    def label(label):
        return '\label{sec:%s}'%label
    
    @staticmethod    
    def nameInTitle(firstName,lastName):
        reversedName = LatexTemplater.reversedName(firstName,lastName)
        return '-- %s --'%reversedName
    
    @staticmethod
    def replaceSpecialCharacters(text):
        return text.replace('ä','\"{a}')
    
    @staticmethod
    def reversedName(firstName,lastName):
        if lastName == '': return firstName
        else:              return '%s, %s'%(lastName,firstName) 
    
    @staticmethod
    def section(title):
        return '\section{%s}'%title
    
    @staticmethod
    def space():
        return '~'
    
    @staticmethod
    def superScript(text):
        return '\supscr{%s}'%text
    
    @staticmethod
    def titlePID(pid):
        return '\pidt{%s}'%pid
    
    @staticmethod
    def textPID(pid):
        return '\pids{%s}'%pid
    
    @staticmethod
    def __itemsWithPrefix(items):
        return ['\item[\emph{\rom{%d}.}] %s'%(i+1,item) for i,item in enumerate(items)]