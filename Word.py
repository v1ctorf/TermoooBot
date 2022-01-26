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
        
        
class Game:
    def __init__(self):
        self.created_at = datetime.now()
        self.remaining_attempts = 6
        
        # self.word_base
        # self.word_scope
        # self.right_letters
        # self.discarded_letters
        # self.moving_letters


game = Game()
print(game.created_at)        