import sys

sys.path.append("..")

from termooobot import TermoooBot

player = TermoooBot()
player.play()
status = '#TermoooBot ' + player.today_stats
player.social.tweet(status)