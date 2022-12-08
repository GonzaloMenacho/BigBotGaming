import discord
import tweepy
import os
from dotenv import load_dotenv

load_dotenv()

consumer_key = os.getenv('TWITTERCONSUMERKEY')
consumer_secret = os.getenv('TWITTERCONSUMERKEYSECRET')
access_token = os.getenv('TWITTERACCESSTOKEN')
access_token_secret = os.getenv('TWITTERACCESSTOKENSECRET')


async def grab_latest_tweet(ctx, username):
    auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True)

    #username = 'DeepLeffen'

    try:
        tweets_list = api.user_timeline(screen_name = username, count = 1, tweet_mode='extended')
        tweet= tweets_list[0]
        await ctx.send(tweet.full_text)
    except:
        await ctx.send(f"The Twitter handle {username} was not found!")