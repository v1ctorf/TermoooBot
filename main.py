import sys

sys.path.append("..")

from termooobot import TermoooBot

player = TermoooBot()
player.play()
status = '#TermoooBot ' + player.today_stats + "\n\npowered by https://github.com/v1ctorf/TermoooBot"
player.social.tweet(status)