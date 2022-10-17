from django.urls import path
import TweetSearch.views as TweetSearchViews

urlpatterns = [    
    path('', TweetSearchViews.index, name='index'),
    path('request/', TweetSearchViews.collector, name='request'),
]