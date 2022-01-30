import sys

sys.path.append("..")

from termooobot import TermoooBot

player = TermoooBot()
player.play()
print(player.today_stats)
player.social.request_tweet(1487842545505910784)

