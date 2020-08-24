class LatexTemplater(object):
    @staticmethod
    def compileListingOf(items):
        prefixedItems = LatexTemplater.__itemsWithPrefix(items)
        return '\begin{itemize}\n%s\n\end{itemize}'%prefixedItems
    
    @staticmethod
    def firstLetterBold(text):
        return '\textbf{%s}%s'%(text[0],text[1:])
    
    @staticmethod
    def genderSymbol(genderIndicator):
        genderSymbols = {'m':'~\Mars','v':'~\Venus'}
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
    def reversedName(firstName,lastName):
        if lastName == '': return firstName
        else:              return '%s, %s'%(lastName,firstName) 
    
    @staticmethod
    def section(title):
        return '\section{%s}'%title
    
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
        return '\item[\emph{\rom{1}.}] %s'%items