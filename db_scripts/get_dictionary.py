import random, requests, csv, sys

sys.path.append("..")

from lxml import html
from Word import Word
from datetime import datetime
from unidecode import unidecode
        

def load_word_list_from_file():    
    file = open("../classified_five_letter_words_pt-br.csv",'r', encoding="utf8")    
    lines = file.readlines()[1100:1120]    
    words = []
    
    for i in lines:    
        print(i)
        line = i.split(',')  
        line[1].replace('\n','')
        
        print(line[0].upper())
        metadata = search_on_dictionary(line[0])          
        print(metadata)
    
        word_content = line[0]
        last_mentioned_on = line[1].strip()
        google_results = None
        
        if isinstance(metadata, list): 
            for m in metadata:                  
                part_of_speech=m['class'].replace(';','.').strip()
                meanings = ' | '.join(m['meanings']).replace(';','.')
                
                word = Word(word_content, last_mentioned_on, google_results, part_of_speech, meanings)
                words.append(word)
                print([word.content, word.part_of_speech, word.meanings])
        else:
            word = Word(word_content, last_mentioned_on, google_results, '', '')
            words.append(word)
            print([word.content, word.part_of_speech, word.meanings])
        
        print('\n')
        
    return words


def search_on_dictionary(word):    
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
    }
        
    url = f'https://significado.herokuapp.com/{word}'         

    response = requests.get(url, headers=headers, stream=True)
    response_json = response.json()
    
    return response_json



def save_file(words, filename):
    with open(filename, mode='w',  newline='\n') as words_file:
        word_writer = csv.writer(words_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        word_writer.writerow(['word', 'last_mentioned_on', 'part_of_speech', 'meanings'])

        for i in words:
            print([i.content, i.last_mentioned_on, i.part_of_speech, i.meanings])
            
            try:
                part_of_speech = unidecode(i.part_of_speech)    
            except:
                part_of_speech = None
                
            try:
                meanings = unidecode(i.meanings)    
            except:
                meanings = None                
            
            word_writer.writerow([i.content, i.last_mentioned_on, part_of_speech, meanings])
            
    print(f'{filename} was successfully created')            


words = load_word_list_from_file()


time_now = datetime.now()
file_date = time_now.strftime("%Y-%m-%d_%H%M%S")
file_name = f'{file_date}_classified_five_letter_words_pt-br.csv'
save_file(words, file_name)
    
    
    