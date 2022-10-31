import discord
import random
import giphy_client
from giphy_client.rest import ApiException
import os
from dotenv import load_dotenv

load_dotenv()


GIPHY_API = os.getenv('GIPHY_API')

async def playGif(ctx,topic):
    api_key = GIPHY_API
    api_instance = giphy_client.DefaultApi()
    # arguments for gifs_search_get
    q = topic  
    rating = 'g'  # filters results based on rating (g, pg, pg-13, r)
    limit = 10

    try:
        # searches all Giphy Gifs based on arguments above
        api_response = api_instance.gifs_search_get(
            api_key, q, limit=limit, rating=rating)
        # select random gif from list[Gif]
        gifs = list(api_response.data)
        gif = random.choice(gifs)
        # sends the orignal image url from the Gif Object
        await ctx.channel.send(gif.images.original.url)
    except ApiException as e:
        print("Error when calling DefaultApi-'>gifs_search_get': %s\n" % e)
