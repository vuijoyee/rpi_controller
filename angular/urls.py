from django.conf.urls import url
from angular.views import AngularTemplateView

urlpatterns = [
    url(r'^templates/(?P<item>[A-Za-z0-9\_\-\.\/]+)\.html$', AngularTemplateView.as_view()),

]