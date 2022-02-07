import sys

sys.path.append("..")

from termooobot import TermoooBot

player = TermoooBot()
player.play()
print('#TermoooBot ' + player.today_stats)
# player.social.tweet(player.today_stats)
#print(player.social.tweet('teste'))
#print(player.social.request_tweet(1488300321789067265))

# https://www.jcchouinard.com/twitter-api/#How_to_Post_Tweets_using_Twitter_API
# https://www.jcchouinard.com/tweepy-basic-functions/