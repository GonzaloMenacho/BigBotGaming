import praw
import os
from dotenv import load_dotenv

load_dotenv()
CLIENT_ID = os.getenv('REDDITCLIENTID')
CLIENT_SECRET = os.getenv('REDDITCLIENTSECRET')
USER_AGENT = os.getenv('REDDITUSERAGENT')

reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT,
)

async def pullRedditPost(ctx, subredditname: str="programmerhumor"):
    try:
        subreddit = reddit.subreddit(subredditname)
        random_submission = subreddit.random()
        await ctx.send(f"Post from r/{subredditname} {random_submission.url}")
    except:
        print(f'some sort of HTTP error has happened, probably from a call to a nonexistant subreddit')
    