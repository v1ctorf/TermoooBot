# TermoooBot

Simple program to solve [Termooo](https://newsbeezer.com/portugaleng/wordle-becomes-viral-and-there-is-already-a-portuguese-version-term-ooo/), a Portuguese version for Wordle.

Requirements: 
----------
+ `pip install Unidecode`
+ [Selenium for Python](https://selenium-python.readthedocs.io/)

Road Map:
-------
+ use the official words data base https://github.com/fserb/pt-br/blob/master/palavras
+ Update history (`last_mentioned_on` column on CSV file)
+ Tweet the results
+ Scrap data from Google to get the number of results, but maybe use [ProtonVPN with Python](https://pypi.org/project/protonvpn-cli/) to disguise the requests. This may be a way to order the guesses according to their relevance
+ Mark missed guesses as valid or invalid words for the game
