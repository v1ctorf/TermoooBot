from lxml import html
import requests, datetime, csv, time

class Word:
    def __init__(self, content, history, google_results):
        self.content = content
        
        if (history == ''):
            self.history = None
        else:
            self.history = datetime.datetime.strptime(history, '%Y-%m-%d')
         
        self.google_results = google_results 


def pyGoogleSearch(word):    
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
    }
        
    let url = f'http://www.google.com/search?q={word}+site%3Abr&hl=en'         

    response = requests.get(url, headers=headers, stream=True)
    response.raw.decode_content = True
    tree = html.parse(response.raw)    
    
    result = tree.xpath('//*[@id="result-stats"]/text()')        
    
    if len(result) > 0:
        result = result[0]            
        about_results = result.split()[1]
    
        return int(about_results.replace(',', '').replace('.', ''))
    
    return None
        
        
def calculate_duration(start_time):
    end_time = datetime.datetime.now()
    total_time = end_time - start_time
    seconds_in_day = 24 * 60 * 60
    time_diff = divmod(total_time.days * seconds_in_day + total_time.seconds, 60)
    
    return time_diff
            

def load_word_list_from_file():    
    file = open("five_letter_words_pt-br.csv",'r', encoding="utf8")    
    lines = file.readlines()[1:]    
    words = []
    
    start_time = datetime.datetime.now()   
    print(start_time)
    
    for i in lines:    
        line = i.split(',')  
        line[1].replace('\n','')
        
        google_results = pyGoogleSearch(line[0])
        
        word = Word(content=line[0], history=line[1].strip(), google_results=google_results)        
        print(f'{word.content},{word.history},{word.google_results}') 
        
        if (google_results != None):
            words.append(word)     
        
    file.close()
    
    time_diff = calculate_duration(start_time)
    
    print(f'-- end {time_diff[0]}m{time_diff[1]}s')    
    
    return words


def save_file(words, filename):
    with open(filename, mode='w',  newline='\n') as words_file:
        word_writer = csv.writer(words_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        word_writer.writerow(['word', 'used_at', 'google_results'])

        for i in words:
            word_writer.writerow([i.content, i.history, i.google_results])  


words = load_word_list_from_file()            