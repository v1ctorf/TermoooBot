import random, sys

sys.path.append("..")

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
    def __init__(self, word: Word):
        self.created_at = datetime.now()
        self.word = word
        # self.attempt_number
        
    def show(self):
        print('    ', end='')        
        print(self.word.content.upper(), end=' ')
        print(f'({self.word.part_of_speech})', end=': ')
        print(self.word.meanings, end=' ')
        
        last_mentioned_on = 'not found'
        
        if self.word.last_mentioned_on != None:
            last_mentioned_on = self.word.last_mentioned_on.strftime("%Y-%m-%d")
            
        print(f'[Last mentioned on: {last_mentioned_on}]')         
        
        
class Game:
    def __init__(self):
        self.created_at = datetime.now()
        self.MAX_ATTEMPTS = 6        
        self.word_base = []
        self.word_scope = []
        self.right_letters = {}
        self.discarded_letters = ''
        self.moving_letters = {}
        self.filtered_words = []        
        self.guesses = []
        
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
        
        
    def filter_words(self, attempt):    
        filtered_words = self.word_scope
        
        for letter, position in self.right_letters.items():
            filtered_words = [w for w in filtered_words if w.content[position] == letter]
            
        for letter, positions in self.moving_letters.items():
            filtered_words = [w for w in filtered_words if letter in w.content]
            for p in positions:            
                filtered_words = [w for w in filtered_words if w.content[p] != letter]                         
                
        filtered_words = [w for w in filtered_words if not set(w.content).intersection(self.discarded_letters)]
        
        if ((len(self.moving_letters) + len(self.right_letters)) <= 2) and attempt < 4:
            filtered_words = [w for w in filtered_words if len(set(w.content)) == 5]    
    
        self.filtered_words = filtered_words
        

    def create_guess(self, attempt):
        self.filter_words(attempt)
        
        if len(self.filtered_words) == 0:
            raise ValueError('Suggestion list is empty: check filters, feedback or database')
            
        word = random.choice(self.filtered_words)         
        return Guess(word) 
    
    
    def show_notes(self):
        right_guesses = list('_____')
        inverse_dict =  {value:key for key, value in self.right_letters.items()}
        
        for i in range(5):
            if i in inverse_dict:
                right_guesses[i] = inverse_dict[i].upper()
            else:
                right_guesses[i] = '_'  
                
        right_guesses = ' '.join(right_guesses)
            
        print('\nNOTES:')
        print(f'    keep these letters at: {right_guesses}')
        print('    discarded letters: ', end='')
        print(list(self.discarded_letters.upper()))    
        print(f'    move these letters from: {self.moving_letters}\n')   
    
        
    def play(self):
        for attempt in range(1, self.MAX_ATTEMPTS + 1):
            print(f'\n* * * ATTEMPT #{attempt} * * * \n')            
            guess = self.create_guess(attempt)
            guess.show()
            right_position_count = 0         
            
            for i, letter in enumerate(guess.word.content):
                if (letter in self.right_letters):
                    right_position_count = right_position_count + 1
                    print('\n"' + letter.upper() + f'" is at position #{i}')
                    continue
                       
                what_happened = ('"' + letter.upper() + '" position is ([R]ight | [O]ther | [D]iscard) ? ')
                feedback = input(what_happened).lower().strip()   
                
                if (feedback == 'r'):
                    right_position_count = right_position_count + 1
                    
                    if letter in self.moving_letters:
                        self.moving_letters.pop(letter, None)
                    
                    self.right_letters[letter] = i                
                elif (feedback == 'o'):
                    if letter in self.moving_letters:
                        self.moving_letters[letter].append(i)
                    else: 
                        self.moving_letters[letter] = [i]
                elif (feedback == 'd'):
                    self.discarded_letters = self.discarded_letters + letter
                else:
                    raise ValueError('feedback {feedback} does not exist')
                    
            if right_position_count == 5:        
                print('\nThe word must be ' + guess.word.content.upper())        
                break
            else:
                self.show_notes()
        
                
        
        
        


game = Game()
game.play()
