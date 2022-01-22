import datetime, random, sys

sys.path.append("..")

from Word import Word
        
        
def load_word_list_from_file():    
    file = open("classified_five_letter_words_pt-br.csv",'r', encoding="utf8")    
    lines = file.readlines()[1:]    
    words = []
    
    for i in lines:    
        line = i.split(',')  
        line[1].replace('\n','')
        
        word = Word(content=line[0], history=line[1].strip(), google_results=None, part_of_speech=line[2].strip())                
        words.append(word)      
        
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

    return filtered_words 



def show_ordered_suggestions(suggestions):
    print('SUGGESTIONS ', end='')
    max_num = 38
    
    #for w in suggestions:
        #print([w.content, w.part_of_speech])
              
    if (len(suggestions) > max_num):
        print('(' + str(max_num) + ' of ' + str(len(suggestions)) + ' possibilities from database):')   
        suggestions = random.sample(suggestions, max_num)
    else:
        random.shuffle(suggestions)
        print('(' + str(len(suggestions)) + ' possibilities from database):')        
        
    for i in suggestions:
        print(i.content, end=' ')
        
        
        
def show_notes(right_position, other_position, discarded):
    print('\nNOTES:')
    print('discarded: ', end='')
    print(list(discarded))
    print(f'keep: {right_position}')
    print(f'move: {other_position}\n')    


    
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
            print(f'\n"{letter}" is at position #{i}')
            continue

        print('\n[R]ight | [O]ther | [D]iscard')                                
        what_happened = (f'what happened to "{letter}"? ')            
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







    
        
        