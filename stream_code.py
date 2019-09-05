from tweepy import Stream, API
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from config import CONSUMER_KEY, CONSUMER_SECRET
from config import ACCESS_TOKEN, ACCESS_TOKEN_SECRET

# OAuth process
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = API(auth)


# listener that handles streaming data
class listener(StreamListener):
    def __init__(self, api=None):
        super().__init__(api=api)
        self.duplicate_avoider = set()
        self.emit = None
    
    def set_funcs(self, emit):
        self.emit = emit

    def on_connect(self):
        print('Stream starting...')

    def on_status(self, status):
        # If the tweet is not a retweet
        if 'RT @' not in status.text:
            if self.emit:
                if status.text not in self.duplicate_avoider:
                    self.emit({'data': f'{status.text}'})
                    self.duplicate_avoider.add(status.text)

    def on_error(self, status):
        print(status)


def getTwitterStream(tracker, emit_func):
    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")

    tweet_listener = listener()
    tweet_listener.set_funcs(emit_func)
    twitterStream = Stream(auth, tweet_listener)
    return twitterStream
  
