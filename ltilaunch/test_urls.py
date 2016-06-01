from django.conf.urls import url

from .views import LaunchView, ConfigView

urlpatterns = [
    url(r'^testlaunch', LaunchView.as_view(), name='testlaunch'),
    url(r'^config/(?P<slug>\w+)/$',
        ConfigView.as_view(template_name='config.xml'),
        name='lti_config_view')
]

