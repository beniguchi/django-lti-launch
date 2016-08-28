from django.conf.urls import url
from . import views

app_name = 'ltilaunch'
urlpatterns = [
    url(r'^config/(?P<slug>\w+)/config.xml$',
        views.ConfigView.as_view(template_name='config.xml'),
        name='lti_config_view')
]
