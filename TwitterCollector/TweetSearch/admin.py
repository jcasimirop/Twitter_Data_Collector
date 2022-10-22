from django.contrib import admin
from TweetSearch.models import Tweet
from import_export.admin import ImportExportModelAdmin

class tweetAdmin(ImportExportModelAdmin):
    list_display=['pk', 't_username', 't_nickname', 't_likes', 't_retweets', 't_followers', 't_verified']
    search_fields=['username']


admin.site.register(Tweet, tweetAdmin)