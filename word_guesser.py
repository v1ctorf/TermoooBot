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



def calculate_letters_distribution(words):
    dict_letters = {}
    
    for word in words:
        for letter in word.content:            
            if letter in dict_letters:
                dict_letters[letter] = dict_letters[letter] + 1
            else:
                dict_letters[letter] = 1
        
    return dict_letters   



def set_words_scope(words):
    scope = [w for w in words if w.part_of_speech != None]    
    scope = [w for w in scope if 'substantivo' in w.part_of_speech or 'adjetivo' in w.part_of_speech] 
    # TODO handle words with history
    return scope



def filter_words(words, right_position, other_position, discarded):    
    filtered_words = words
    
    for letter, position in right_position.items():
        filtered_words = [w for w in filtered_words if w.content[position] == letter]
        
    for letter, positions in other_position.items():
        filtered_words = [w for w in filtered_words if letter in w.content]
        for p in positions:            
            filtered_words = [w for w in filtered_words if w.content[p] != letter]                         
            
    filtered_words = [w for w in filtered_words if not set(w.content).intersection(discarded)]
    
    if ((len(other_position) + len(right_position)) <= 2):
        filtered_words = [w for w in filtered_words if len(set(w.content)) == 5]    
        
    filtered_words = merge_different_meanings(filtered_words)           

    return filtered_words 


# is this redundant?
def merge_different_meanings(filtered_words):    
    unique_content = set([w.content for w in filtered_words])
    merged_words = []
    
    for u in unique_content:
        words_to_be_merged = [w for w in filtered_words if w.content == u]        
            
        last_mentioned_on = random.choice([w.last_mentioned_on for w in words_to_be_merged])                
        google_results = None
        part_of_speech = ' | '.join([w.part_of_speech for w in words_to_be_merged])
        meanings = ' | '.join([w.meanings for w in words_to_be_merged])
        
        word = Word(u, last_mentioned_on, google_results, part_of_speech, meanings)                
        
        merged_words.append(word)     

    return merged_words       
        


def show_ordered_suggestions(suggestions):
    print('SUGGESTIONS ', end='')
    max_num = 8
              
    if (len(suggestions) > max_num):
        print('(' + str(max_num) + ' of ' + str(len(suggestions)) + ' words from database):')   
        suggestions = random.sample(suggestions, max_num)
    else:
        random.shuffle(suggestions)
        print('(' + str(len(suggestions)) + ' word(s) from database):')        
        
    for i in suggestions:
        print('    ', end='')        
        print(i.content.upper(), end=' ')
        print(f'({i.part_of_speech})', end=': ')
        print(i.meanings, end=' ')
        
        last_mentioned_on = 'not found'
        
        if i.last_mentioned_on != None:
            last_mentioned_on = i.last_mentioned_on.strftime("%Y-%m-%d")
            
        print(f'[Last mentioned on: {last_mentioned_on}]\n')
        
        
        
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

letters_distro = calculate_letters_distribution(words)

end_game = False
right_position = {}
other_position = {}
discarded = ''

while not end_game:
    show_notes(right_position, other_position, discarded)    
    suggestions = filter_words(words, right_position, other_position, discarded)      
    show_ordered_suggestions(suggestions)
            
    word = input('\ntype your attempt: ').lower().strip()
    result = input(f'did "{word}" work? [y|n]: ').lower().strip()    
    
    if result == 'y':
        end_game = True
        print('congratulations')
        continue
    
    for i, letter in enumerate(word):
        if (letter in right_position):
            print('\n"' + letter.upper() + f'" is at position #{i}')
            continue

        print('\n[R]ight | [O]ther | [D]iscard')                                
        what_happened = ('what happened to "' + letter.upper() + '"? ')                
        feedback = input(what_happened).lower().strip()   
        
        if (feedback == 'r'):
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







    
        
        