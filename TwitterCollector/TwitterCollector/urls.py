from django.contrib import admin
from django.urls import include, path
import TweetSearch.views as TweetSearchViews

urlpatterns = [
    path('index/', include('TweetSearch.urls')),
    path('admin/', admin.site.urls),

]