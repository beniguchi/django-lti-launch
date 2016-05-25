from django.conf.urls import url

from ltilaunch.views import LaunchView

urlpatterns = [
    url(r'^testlaunch', LaunchView.as_view(), name='testlaunch')
]