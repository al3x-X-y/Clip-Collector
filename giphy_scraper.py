import time
import giphy_client
from giphy_client.rest import ApiException
from pprint import pprint

def gif (ctx, search):

    api_key = "XbIwaoR4IQwNNcGMvgTdYGtB8kMq03EA";
    api_instance = giphy_client.DefaultApi()

    try :
        api_response = api_instance.gifs_search_get(api_key, search, limit=5)
        lst = []
        for i in range(5):
            lst.append(api_response.data[i].url)
        await ctx.channel.send(lst)
    except ApiException as e:
        print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)

gif('abc',"cat")
