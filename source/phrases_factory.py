ENGLISH = ('From a relationship between',
           'and',
           'was brought forth',
           'was baptised on the',
           '\supscr{th} of December',
           'before the catholic church of the',
           'parish at')  
    
DUTCH = ('Uit een relatie tussen',
         'en',
         'is voortgebracht',
         'is gedoopt op de',
         '\supscr{de} december',
         'voor de katholieke kerk van de',
         'parochie te')

GERMAN = ('Aus einer Beziehung zwischen',
         'und',
         'ist geboren worden',
         'ist am',
         '. Dezember',
         'getauft vor dem katholischen Kirche der',
         'Pfarrei zu')

PHRASES = {'en':ENGLISH,'nl':DUTCH,'de':GERMAN}

class PhrasesFactory(object):
    @staticmethod
    def inLanguage(language):
        return PHRASES[language]
        
      
