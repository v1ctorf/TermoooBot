import random, requests, csv, sys

sys.path.append("..")

from lxml import html
from Word import Word
from datetime import datetime


def search_on_google(word):    
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
    }
        
    url = f'http://www.google.com/search?q={word}+site%3Abr&hl=en'
    response = requests.get(url, headers=headers, stream=True)
    response.raw.decode_content = True
    tree = html.parse(response.raw)    
    
    result = tree.xpath('//*[@id="result-stats"]/text()')        
    
    if len(result) > 0:
        result = result[0]            
        about_results = result.split()[1]
    
        return int(about_results.replace(',', '').replace('.', ''))
    
    return None
        
            

def load_word_list_from_file():    
    file = open("../classified_five_letter_words_pt-br.csv",'r', encoding="utf8")    
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


def save_file(words, filename):
    with open(filename, mode='w',  newline='\n') as words_file:
        word_writer = csv.writer(words_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        word_writer.writerow(['word', 'last_mentioned_on', 'part_of_speech', 'meanings'])

        for i in words:
            word_writer.writerow([i.content, i.last_mentioned_on, i.part_of_speech, i.meanings])
            
    print(f'{filename} was successfully created')   
    
    

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
    


words = load_word_list_from_file()
print(len(words))

words = [w for w in words if w.part_of_speech != None]
print(len(words))

words = merge_different_meanings(words)
print(len(words))

sample = random.sample(words, 20)  

for i in sample:
    print([i.content, i.last_mentioned_on, i.part_of_speech, i.meanings],end='\n\n')

time_now = datetime.now()
file_date = time_now.strftime("%Y-%m-%d_%H%M%S")
file_name = f'{file_date}_classified_five_letter_words_pt-br.csv'
save_file(words, file_name)          