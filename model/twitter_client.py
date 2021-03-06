# -------------------------------------------------------------------
# Furuikeya Twitter Client
# -------------------------------------------------------------------
#
#
#   Author : PLIQUE Guillaume
#   Version : 1.0

# Dependencies
#=============
import re
import random
import time
import sys

from twitter import Twitter, OAuth
from colifrapy import Model
from pprint import pprint

# Main Class
#=============
class TwitterClient(Model):

    # Properties
    t = None
    twopts = {
        'lang' : 'en',
        'result_type' : 'recent',
        'count' : '100',
        'include_entities' : 'false'
    }

    # Constructor
    def __init__(self):

        # Announcing
        self.log.write('twitter:open')

        # Regsitering Oauth
        self.t = Twitter(auth=OAuth(
            self.settings.twitter['oauth_token'],
            self.settings.twitter['oauth_secret'],
            self.settings.twitter['consumer_key'],
            self.settings.twitter['consumer_secret']
        ))

    # Find Tweets
    def findTweets(self, kigo):

        # Pausing to avoid being kicked too fast
        time.sleep(1)

        # Announcing
        self.log.write('twitter:fetch', variables={'kigo' : kigo})

        # Options
        self.twopts['q'] = kigo
        search = self.t.search.tweets(**self.twopts)

        # Setting the next page
        try:
            next_results = re.search(r'max_id=(.*?)&', search['search_metadata']['next_results'])
            self.twopts['max_id'] = next_results.group(1)
        except KeyError:
            self.log.write('twitter:end_results', variables={'kigo' : kigo})

        # Yielding
        random.shuffle(search['statuses'])
        for tweet in search['statuses']:
            yield tweet['text']