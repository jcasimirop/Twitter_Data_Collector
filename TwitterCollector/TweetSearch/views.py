from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
import requests
import json
from datetime import datetime
from django.shortcuts import render
from django.conf import settings
from django.views.generic.base import TemplateView
from django.views.decorators.csrf import csrf_exempt
from TweetSearch.models import Tweet, Hashtag

api_key = settings.API_KEY
api_key_secret = settings.API_KEY_SECRET
bearer_token = settings.BEARER_TOKEN

path = './'
file_name = 'placeholder_name'


search_url = "https://api.twitter.com/2/tweets/search/recent"

def createFile(path, file_name, data):
    pathAndName = './'+path+'/'+file_name+'.json'
    with open(pathAndName, 'w') as pdr:
        json.dump(data, pdr)

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def create_query(user_hashtag):
    # Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
    # expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
    query_params = {'query': '#'+ user_hashtag +' -is:retweet lang:en',
                    'user.fields': 'username,verified,public_metrics',
                    'tweet.fields': 'author_id,created_at,text,entities,public_metrics',
                    'expansions': "author_id",
                    'max_results': 10,}

    return (query_params)

@csrf_exempt
def collector(request):
    try:
        user_hashtag = str(request.POST['hashtag'])
        print(user_hashtag, type(user_hashtag))
        # username = request.POST['username']
        # nickname = request.POST['nickname']
        # likes = request.POST['likes']
        # retweets = request.POST['retweets']
        # followers = request.POST['followers']
        # verified = request.POST['verified']

        json_response = connect_to_endpoint(search_url, create_query(user_hashtag))

        for t_tweet, t_user in zip(json_response['data'], json_response['includes']['users']):
            print(t_tweet['created_at'])
            date_string = datetime.strptime(t_tweet['created_at'], '%Y-%m-%dT%H:%M:%S.000Z')
            Tweet.objects.create(
                t_id = t_tweet['author_id'],
                t_text = t_tweet['text'],
                t_username = t_user['username'],
                t_nickname = t_user['name'],
                t_likes = t_tweet['public_metrics']['like_count'],
                t_retweets = t_tweet['public_metrics']['retweet_count'],
                t_followers = t_user['public_metrics']['followers_count'],
                t_verified = t_user['verified'],
                t_date = date_string,
            )
            hashtags = t_tweet['entities']['hashtags']
            for hashtag in hashtags:
                Hashtag.objects.create(h_hashtag=hashtag['tag'], h_tweet = Tweet.objects.last())

        createFile(path, file_name, json_response)

        # print(json.dumps(json_response, indent=4, sort_keys=True))
        return render (request, 'search.html', {'tweets':Tweet.objects.all()})
    except Exception as e:
        return render (request, 'search.html', {'data':''})

def index(request):
    context={}
    return render(request,'index.html', context)
    
    
    
# class indexView(TemplateView):
#     template_name = 'TwitterCollector/index.html'
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context

# class tableView(TemplateView):
#     template_name = 'TwitterCollector/table.html'
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context