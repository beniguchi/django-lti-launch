from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models


class LTIToolConsumer(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    oauth_consumer_key = models.TextField()
    oauth_consumer_secret = models.TextField()
    tool_consumer_instance_guid = models.TextField()


class LTIUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                primary_key=True,
                                on_delete=models.CASCADE)
    lti_tool_consumer = models.ForeignKey(LTIToolConsumer)
    last_launch_parameters = JSONField()
    last_launch_time = models.DateTimeField()
