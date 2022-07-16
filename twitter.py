import os

try:
    import tweepy
except ImportError:
    raise ImportError("pip install tweepy")


class Twitter:
    def __init__(self):
        auth = tweepy.OAuthHandler(
            os.environ["Twitter_consumer_key"],
            os.environ["Twitter_consumer_secret"]
        )
        auth.set_access_token(
            os.environ["Twitter_access_token"],
            os.environ["Twitter_access_token_secret"]
        )
        self.__twitter_api = tweepy.API(auth)

    def post_tweet(self, msg: str):
        """自垢でツイート"""
        self.__twitter_api.update_status(msg)

    def get_UsersTweets_obj(self, account_id: str, count: int, include_rts_flg: bool):
        """ user tweet object
            >>>  # exsample
                tweets = Twitter().get_UsersTweets_obj('YahooNewsTopics', 5, False)
        """
        tweets = list(
            tweepy.Cursor(
                self.__twitter_api.user_timeline,
                screen_name=account_id,
                include_rts=include_rts_flg,
                tweet_mode="extended"
            ).items(count))
        tweets.reverse()
        return tweets

    def get_TimelineTweets_obj(self, list_id: int, count: int, include_rts_flg: bool):
        """ TL tweet object
            >>> # exsample
                tweets = Twitter().get_TimelineTweets_obj(
                    list_id='YahooNewsTopics', 7, True)"""
        tweets_obj = self.__twitter_api.list_timeline(
            list_id=list_id,
            count=count,
            include_rts=include_rts_flg,
            tweet_mode="extended")
        return tweets_obj
