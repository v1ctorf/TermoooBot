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
       
        
    def update(self, **params):
        print('\n\nAntes:')
        print(self.__dict__)
        params_list = list(self.__dict__.keys())
        
        update_params = {}
        
        for i in params_list:
            update_params[i] = params[i] if i in params else self.__dict__[i]            
        
        print('\n\nDepois:')
        print(update_params)
        


class WordBase:
    def __init__(self):
        self.word_base = []
        self.load()
        
    def load(self):
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

    
        