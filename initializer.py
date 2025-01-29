import os
from twitchAPI.twitch import Twitch
import tweepy
from mastodon import Mastodon
import bluesky_service as BlueSkyService

class SocialMediaServices:
    def __init__(self):
        self.twitch = None
        self.mastodon = None
        self.twitter_api = None
        self.bluesky = None
        self.initialize_services()

    def initialize_services(self):
        self._initialize_twitch()
        self._initialize_mastodon()
        self._initialize_twitter()
        self._initialize_bluesky()

    def _initialize_twitch(self):
        self.twitch = Twitch(os.getenv('TWITCH_CLIENT_ID'), os.getenv('TWITCH_CLIENT_SECRET'))
        self.twitch.authenticate_app([])
        print("Successfully authenticated with Twitch API")

    def _initialize_mastodon(self):
        self.mastodon = Mastodon(
            client_id=os.getenv('MASTODON_CLIENT_ID'),
            client_secret=os.getenv('MASTODON_CLIENT_SECRET'),
            access_token=os.getenv('MASTODON_ACCESS_TOKEN'),
            api_base_url=os.getenv('MASTODON_API_BASE_URL')
        )
        print("Successfully authenticated with Mastodon API")

    def _initialize_twitter(self):
        if os.getenv('TWITTER_ENABLE_POSTING', 'false').lower() == 'true':
            auth = tweepy.OAuthHandler(
                os.getenv('TWITTER_CONSUMER_KEY'),
                os.getenv('TWITTER_CONSUMER_SECRET')
            )
            auth.set_access_token(
                os.getenv('TWITTER_ACCESS_TOKEN'),
                os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
            )
            self.twitter_api = tweepy.API(auth)
            print("Successfully authenticated with Twitter API")

    def _initialize_bluesky(self):
        self.bluesky = BlueSkyService()

    def get_services(self):
        return self.twitch, self.mastodon, self.twitter_api, self.bluesky