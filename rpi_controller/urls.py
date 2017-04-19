from django.conf.urls import url, include
from django.views.generic.base import TemplateView

from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

from rest_framework_jwt.views import obtain_jwt_token


urlpatterns = [
    url(r'^auth/token/', obtain_jwt_token),
    url(r'^ng/', include('angular.urls')),
    url(r'^api/', include('api.urls')),
    url('^register/', CreateView.as_view(
        template_name='angular/auth/register.html',
        form_class=UserCreationForm,
        success_url='/'
    )),
]

urlpatterns += [
    url(r'', TemplateView.as_view(template_name='angular/index.html'))
]
