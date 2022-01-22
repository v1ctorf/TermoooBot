from lxml import html
from word import Word
import datetime, random, requests, csv
        

def load_word_list_from_file():    
    file = open("five_letter_words_pt-br.csv",'r', encoding="utf8")    
    lines = file.readlines()[1:]    
    words = []
    
    for i in lines:    
        line = i.split(',')  
        line[1].replace('\n','')
        
        metadata = search_on_dictionary(line[0])
        
        print([line[0], metadata])        
        
        if isinstance(metadata, list) and 'class' in metadata[0]:
            part_of_speech = metadata[0]['class']        
        else:
            part_of_speech = ''
        
        word = Word(content=line[0], history=line[1].strip(), google_results=None, part_of_speech=part_of_speech.strip())                
        words.append(word) 
        
        print([word.content, word.part_of_speech])
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
        word_writer = csv.writer(words_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        word_writer.writerow(['word', 'history', 'part_of_speech'])

        for i in words:
            word_writer.writerow([i.content, i.history, i.part_of_speech])
            


words = load_word_list_from_file()
save_file(words, 'classified_five_letter_words_pt-br.csv')
    
    
    