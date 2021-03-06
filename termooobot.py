import random, sys, time, pyperclip

sys.path.append("..")

from datetime import datetime
from selenium import webdriver
from unidecode import unidecode
from social import SocialMedia
from word import Word, WordBase
        
        
        
class Guess:
    def __init__(self, word: Word):
        self.created_at = datetime.now()
        self.word = word        
        
        
    def show(self):
        print('    ', end='')        
        print(self.word.content.upper(), end=' ')
        print(f'({self.word.part_of_speech})', end=': ')
        print(self.word.meanings, end=' ')
        
        last_mentioned_on = 'not found'
        
        if self.word.last_mentioned_on != None:
            last_mentioned_on = self.word.last_mentioned_on.strftime("%Y-%m-%d")
            
        print(f'[Last mentioned on: {last_mentioned_on}]')
        
        
        
class TermoooBot:
    def __init__(self):
        self.created_at = datetime.now()
        self.MAX_ATTEMPTS = 6        
        self.word_base = WordBase()
        self.word_scope = []
        self.right_letters = []
        self.wrong_letters = ''
        self.moving_letters = {}
        self.filtered_words = []        
        self.guesses = []
        self.driver = None    
        self.today_stats = None        
        self.social = SocialMedia()
                   
        self.set_word_scope()
        self.set_right_letters()          
    
    
    def set_driver(self):
        path = "C:\Python\geckodriver\geckodriver.exe"
        self.driver = webdriver.Firefox(executable_path = path)        
       
        
    def open_page(self):
        self.driver.get("https://term.ooo")
        assert "Termo" in self.driver.title
        time.sleep(1)
        help_modal = self.driver.find_element_by_id('help')
        help_modal.click()
        time.sleep(2)
        
    
    def close_page(self):
        self.driver.close() 
        
        
    def set_right_letters(self):
        self.right_letters = [None for i in range(5)]
        
        
    def count_right_letters(self):
        return len(list(filter(None, self.right_letters)))


    def set_word_scope(self):
        word_list = self.word_base.get()
        
        scope = [w for w in word_list if w.part_of_speech != None]    
        self.word_scope = [w for w in scope if 'substantivo' in w.part_of_speech or 'adjetivo' in w.part_of_speech or 'verbo' in w.part_of_speech]
        self.word_scope = [w for w in self.word_scope if w.last_mentioned_on == None]    
        # todo mind last_mentioned only if it's older than today
        
        
    def filter_words(self, attempt):    
        filtered_words = self.word_scope

        for i in range(0, len(self.right_letters)):
            if self.right_letters[i] != None:
                right = self.right_letters[i]
                filtered_words = [w for w in filtered_words if w.content[i] == right]            
            
        for letter, positions in self.moving_letters.items():
            filtered_words = [w for w in filtered_words if letter in w.content]
            for p in positions:            
                filtered_words = [w for w in filtered_words if w.content[p] != letter]                         
                
        filtered_words = [w for w in filtered_words if not set(w.content).intersection(self.wrong_letters)]      
        
        if (len(self.moving_letters) + self.count_right_letters()) <= 2 and attempt < 4:
            filtered_words = [w for w in filtered_words if len(set(w.content)) == 5]    
    
        self.filtered_words = filtered_words        


    def take_guess(self, attempt):
        self.filter_words(attempt)
        
        if len(self.filtered_words) == 0:
            raise ValueError('Suggestion list is empty: check filters, feedback or database')
            
        word = random.choice(self.filtered_words)   
        return Guess(word)    
    
    
    def submit_guess(self, guess: Guess):
        for letter in guess.word.content:
            letter_key = self.driver.find_element_by_id(f'kbd_{letter}')
            letter_key.click()
            time.sleep(1)
                    
        enter_key = self.driver.find_element_by_id('kbd_enter')
        enter_key.click()  
        time.sleep(3)
    
    
    def show_notes(self):
        right_guesses = [l.upper() if l else '_' for l in self.right_letters]                
        right_guesses = ' '.join(right_guesses)
            
        print('\nNOTES:')
        print(f'    keep these letters at: {right_guesses}')
        print('    discarded letters: ', end='')
        print(list(self.wrong_letters.upper()))    
        print(f'    move these letters from: {self.moving_letters}\n')  
        
        
    def mark_letter_as_right(self, letter, position):
        if letter in self.moving_letters:
            self.moving_letters.pop(letter, None)
        
        self.right_letters[position] = letter
        
        
    def mark_letter_as_place(self, letter, position):
        if letter in self.moving_letters:
            self.moving_letters[letter].append(position)
        else: 
            self.moving_letters[letter] = [position]
            
            
    def mark_letter_as_wrong(self, letter):
        if letter not in self.right_letters and letter not in self.moving_letters.keys():
            self.wrong_letters = self.wrong_letters + letter   
    
        
    def check_results(self):        
        rows = self.driver.find_elements_by_class_name('row')
        page_input = rows[len(self.guesses) - 1]
        input_letters = page_input.find_elements_by_class_name('letter')        
        discard = []
        
        for i, letter_element in enumerate(input_letters):
            result = letter_element.get_attribute('class').split(' ')[1]
            letter = unidecode(letter_element.text.lower())
            
            if result == 'right':                
                self.mark_letter_as_right(letter, i)
            elif result == 'place':
                self.mark_letter_as_place(letter, i)
            elif result == 'wrong':
                discard.append(letter)
            else:
                raise ValueError('Can\'t process result from page.')
        else:
            for letter in discard:
                self.mark_letter_as_wrong(letter)      


    def set_today_stats(self):
        stats_share = self.driver.find_element_by_id('stats_share')
        stats_share.click()        
        self.today_stats = pyperclip.paste()
        time.sleep(2)
        
        
    def play(self):
        self.set_driver()
        self.open_page()
        
        for attempt in range(1, self.MAX_ATTEMPTS + 1):            
            print(f'\n* * * ATTEMPT #{attempt} * * * \n')            
            guess = self.take_guess(attempt)
            self.guesses.append(guess)            
            guess.show()    
            self.submit_guess(guess)            
            self.check_results()
                   
            if self.count_right_letters() == 5:        
                print('\nThe word must be ' + guess.word.content.upper())   
                self.set_today_stats()                
                self.word_base.mark_as_mentioned(guess.word)
                break
            else:
                self.show_notes()
        else:
            if self.count_right_letters() < 5:
                print(f'The word could not be guessed before {self.MAX_ATTEMPTS}')
                
        self.close_page()
        
        if self.today_stats != None:
            status = '#TermoooBot ' + self.today_stats + "\n\npowered by https://github.com/v1ctorf/TermoooBot"
            self.social.tweet(status)