import datetime

class Word:
    def __init__(self, content, history, google_results, part_of_speech):
        self.content = content
        
        if (history == ''):
            self.history = None
        else:
            self.history = datetime.datetime.strptime(history[:10], '%Y-%m-%d')
         
        self.google_results = google_results 
        
        if (part_of_speech == '' or part_of_speech == None):
            self.part_of_speech = None
        else:            
            self.part_of_speech = part_of_speech   