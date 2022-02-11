# TermoooBot

Simple program to solve [Term.ooo](https://newsbeezer.com/portugaleng/wordle-becomes-viral-and-there-is-already-a-portuguese-version-term-ooo/), a Portuguese version for Wordle.

Requirements: 
----------
+ Install `pip install Unidecode`
+ Install [Selenium for Python](https://selenium-python.readthedocs.io/)
+ Install `pip install tweepy`
+ Create a `config.yml` following `config.yml.example`
+ Set `config.yml` with your [Twitter App Credentials](https://www.jcchouinard.com/twitter-api-credentials/)

Road Map:
-------
+ Use the [official words data base](https://github.com/fserb/pt-br/blob/master/palavras)
+ Update history (`last_mentioned_on` column on CSV file)
+ Make a simulator considering a significant amount of unique guesses
+ Implement a smarter guessing strategy
