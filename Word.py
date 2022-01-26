from datetime import datetime

class Word:
    def __init__(self, content, last_mentioned_on, google_results, part_of_speech, meanings):
        self.content = content
        
        if last_mentioned_on == '' or last_mentioned_on == None:
            self.last_mentioned_on = None
        elif isinstance(last_mentioned_on, datetime):
            self.last_mentioned_on = last_mentioned_on                        
        else:
            self.last_mentioned_on = datetime.strptime(last_mentioned_on[:10], '%Y-%m-%d')
         
        self.google_results = google_results 
        
        if (part_of_speech == '' or part_of_speech == None):
            self.part_of_speech = None
        else:            
            self.part_of_speech = part_of_speech   
            
        self.meanings = meanings
        
        
        
class Guess:
    def __init__(self):
        self.created_at = datetime.now()
        # self.attempt_number
        # self.word        
        pass
        
        
        
class Game:
    def __init__(self):
        self.created_at = datetime.now()
        self.word_base = []
        self.word_scope = []
        self.right_letters = {}
        self.discarded_letters = ''
        self.moving_letters = {}
        
        self.set_word_base()        
        self.set_word_scope()   
        
       
    def set_word_base(self):
        file = open("classified_five_letter_words_pt-br.csv",'r', encoding="utf8")    
        lines = file.readlines()[1:]            
        
        for i in lines:    
            line = i.split(';')   
            content = line[0].strip()
            last_mentioned_on =  line[1].replace('\n','').strip()
            google_results = None        
            part_of_speech = line[2].strip()
            meanings = line[3].replace('\n','').strip()            
            word = Word(content, last_mentioned_on, google_results, part_of_speech, meanings)            
            self.word_base.append(word)                  
            
        file.close()    
        

    def set_word_scope(self):
        scope = [w for w in self.word_base if w.part_of_speech != None]    
        self.word_scope = [w for w in scope if 'substantivo' in w.part_of_speech or 'adjetivo' in w.part_of_speech] 
        # TODO handle words with history         
        
        # self.guesses        
        
        
        


game = Game()
print(len(game.word_scope))