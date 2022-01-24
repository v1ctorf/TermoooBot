# How To Cheat In Termo

Simple program to solve [Termooo](https://newsbeezer.com/portugaleng/wordle-becomes-viral-and-there-is-already-a-portuguese-version-term-ooo/), a Portuguese version for Wordle.

Requirements: `pip install Unidecode`

Road Map:
-------
+ Ask user if they want to update history (`last_mentioned_on` column on CSV file)
+ Use Selenium from Python to play directly on the website, like [here](https://stackoverflow.com/questions/30615157/sending-javascript-command-from-python-shell)
+ Scrap data from Google to get the number of results, but maybe use [ProtonVPN with Python](https://pypi.org/project/protonvpn-cli/) to disguise the requests. This may be a way to order the guesses according to their relevance
+ Consider words with history
+ Tweet the results
+ Mark missed guesses as valid or invalid words for the game
