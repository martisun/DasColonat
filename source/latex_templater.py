class LatexTemplater(object):
    __nonTrivialMethods = ['genderSymbol']
    
    def evaluate(self,method,arguments):
        if not self.__areAllArgumentsTrivial(arguments)\
        or method in self.__nonTrivialMethods: 
            return getattr(self,method)(*arguments)    
        else: return ''
    
    @staticmethod
    def bold(text):
        return '\textbf{%s}'%text
    
    @staticmethod
    def compileListingOf(templateItems):
        prefixedItems = LatexTemplater.__itemsWithPrefix(templateItems)
        joinedItems   = '\n'.join(prefixedItems)
        return '\begin{itemize}\n%s\n\end{itemize}'%joinedItems
    
    @staticmethod
    def firstLetterBold(text):
        firstLetter = LatexTemplater.bold(text[0])
        remainder   = text[1:]
        return firstLetter+remainder
    
    @staticmethod
    def genderSymbol(genderIndicator):
        genderSymbols = {'m':'\Mars','f':'\Venus','':'?'}
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
    def space(*arg):
        if len(arg) == 0: return '~'
        elif arg[0] == '': return ''
        else:              return ' '
    
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
    def __itemsWithPrefix(templateItems):
        return [LatexTemplater.__itemWithPrefix(i,templateItem)
                for i,templateItem in enumerate(templateItems)]
    
    @staticmethod
    def __itemWithPrefix(index,templateItem):
        templateItemText = templateItem.getText()
        return '\item[\emph{\rom{%d}.}] %s'%(index+1,templateItemText)
    
    @staticmethod
    def __areAllArgumentsTrivial(arguments):
        return len(arguments) != 0 and all([argument=='' for argument in arguments])