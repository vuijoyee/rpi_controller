from django.conf.urls import url, include
from django.contrib.auth.views import login


urlpatterns = [
    #url(r'', login),
    url(r'^v1/', include('api.v1.urls')),
    # url(r'^v2/', include('api.v2.urls')),
]