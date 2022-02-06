import sys

sys.path.append("..")

from termooobot import TermoooBot

player = TermoooBot()
player.play()
print('#TermoooBot ' + player.today_stats)
# player.social.tweet(player.today_stats)
# print(player.social.tweet('teste'))
# # print(player.social.request_tweet(1488300321789067265))

## https://stackoverflow.com/questions/70403237/getting-bad-request-for-twitter-request-token-endpoint-and-invalid-request-for-c