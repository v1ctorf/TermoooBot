import yaml, tweepy

class SocialMedia:    
    def __init__(self):
        self.auth = None        
        self.api = None
        self.is_tweeting_allowed = None        
        self.set_auth()
        self.set_api()
        
        
    def set_auth(self):
        with open('./config.yml') as f:    
            config_vars = yaml.safe_load(f)
            
        api_key = config_vars['api_key']
        api_secrets = config_vars['api_key_secret']
        access_token = config_vars['access_token']
        access_secret = config_vars['access_token_secret']
        
        self.is_tweeting_allowed = config_vars['tweeting_allowed']        
        self.auth = tweepy.OAuthHandler(api_key, api_secrets)
        self.auth.set_access_token(access_token, access_secret) 
        
    
    def set_api(self):        
        self.api = tweepy.API(self.auth)
        
    
    def tweet(self, status):
        if self.is_tweeting_allowed == False:
            print('Not allowed to tweet; set config.yml')
            return
            
        tweet = self.api.update_status(status=status, card_uri='tombstone://card')  
        print(f'Tweeted about it @ {tweet.created_at}')