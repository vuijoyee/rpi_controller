from django.conf.urls import url, include
from django.views.generic.base import TemplateView

from rest_framework_jwt.views import obtain_jwt_token


urlpatterns = [
    url(r'^auth/token/', obtain_jwt_token),
    url(r'^api/', include('angular.urls')),
]

urlpatterns += [
    url(r'', TemplateView.as_view(template_name='angular/index.html'))
]
