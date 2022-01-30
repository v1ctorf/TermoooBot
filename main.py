import sys

sys.path.append("..")

from termooobot import TermoooBot

player = TermoooBot()
player.play()
print(player.today_stats)

