import datetime, random, sys

sys.path.append("..")

from Word import Word
        
        
def load_word_list_from_file():    
    file = open("classified_five_letter_words_pt-br.csv",'r', encoding="utf8")    
    lines = file.readlines()[1:]    
    words = []
    
    for i in lines:    
        line = i.split(';')                                
        
        content = line[0].strip()
        last_mentioned_on =  line[1].replace('\n','').strip()
        google_results = None        
        part_of_speech = line[2].strip()
        meanings = line[3].replace('\n','').strip()
        
        word = Word(content, last_mentioned_on, google_results, part_of_speech, meanings)                
        
        words.append(word)      
        
    file.close()            
        
    return words



def set_words_scope(words):
    scope = [w for w in words if w.part_of_speech != None]    
    scope = [w for w in scope if 'substantivo' in w.part_of_speech or 'adjetivo' in w.part_of_speech] 
    # TODO handle words with history
    return scope



def filter_words(words, right_position, other_position, discarded, attempt):    
    filtered_words = words
    
    for letter, position in right_position.items():
        filtered_words = [w for w in filtered_words if w.content[position] == letter]
        
    for letter, positions in other_position.items():
        filtered_words = [w for w in filtered_words if letter in w.content]
        for p in positions:            
            filtered_words = [w for w in filtered_words if w.content[p] != letter]                         
            
    filtered_words = [w for w in filtered_words if not set(w.content).intersection(discarded)]
    
    if ((len(other_position) + len(right_position)) <= 2) and attempt < 4:
        filtered_words = [w for w in filtered_words if len(set(w.content)) == 5]    

    return filtered_words 



def guess_word_from_suggestion_list(suggestions):
    if len(suggestions) == 0:
        raise ValueError('Suggestion list is empty: check filters, feedback or database')
        
    guess = random.choice(suggestions)
    
    return guess
           


def show_guess(guess):            
    print('    ', end='')        
    print(guess.content.upper(), end=' ')
    print(f'({guess.part_of_speech})', end=': ')
    print(guess.meanings, end=' ')
    
    last_mentioned_on = 'not found'
    
    if guess.last_mentioned_on != None:
        last_mentioned_on = guess.last_mentioned_on.strftime("%Y-%m-%d")
        
    print(f'[Last mentioned on: {last_mentioned_on}]')
        
        
        
def show_notes(right_position, other_position, discarded):
    right_guesses = list('_____')
    inverse_dict =  {value:key for key, value in right_position.items()}
    
    for i in range(5):
        if i in inverse_dict:
            right_guesses[i] = inverse_dict[i].upper()
        else:
            right_guesses[i] = '_'  
            
    right_guesses = ' '.join(right_guesses)
        
    print('\nNOTES:')
    print(f'    keep these letters at: {right_guesses}')
    print('    discarded letters: ', end='')
    print(list(discarded.upper()))    
    print(f'    move these letters from: {other_position}\n')   
    

    
words = load_word_list_from_file()
words = set_words_scope(words)

end_game = False
right_position = {}
other_position = {}
discarded = ''
remaining_attempts = 6

for attempt in range(1, remaining_attempts + 1):
    print(f'\n* * * ATTEMPT #{attempt} * * * \n')     
    
    suggestions = filter_words(words, right_position, other_position, discarded, attempt) 
    word = guess_word_from_suggestion_list(suggestions)
    show_guess(word)           
    right_position_count = 0
    
    for i, letter in enumerate(word.content):
        if (letter in right_position):
            right_position_count = right_position_count + 1
            print('\n"' + letter.upper() + f'" is at position #{i}')
            continue
               
        what_happened = ('"' + letter.upper() + '" position is ([R]ight | [O]ther | [D]iscard) ? ')
        feedback = input(what_happened).lower().strip()   
        
        if (feedback == 'r'):
            right_position_count = right_position_count + 1
            
            if letter in other_position:
                other_position.pop(letter, None)
            
            right_position[letter] = i                
        elif (feedback == 'o'):
            if letter in other_position:
                other_position[letter].append(i)
            else: 
                other_position[letter] = [i]
        elif (feedback == 'd'):
            discarded = discarded + letter
        else:
            raise ValueError('feedback {feedback} does not exist')
            
    if right_position_count == 5:        
        print('\nThe word must be ' + word.content.upper())        
        break
    else:
        show_notes(right_position, other_position, discarded)       