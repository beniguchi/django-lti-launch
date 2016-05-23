from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models


class LTITenant(models.Model):
    tenant_short_name = models.CharField(max_length=50)
    tenant_description = models.TextField(blank=True)
    oauth_consumer_key = models.TextField()
    oauth_consumer_secret = models.TextField()
    tool_consumer_instance_guid = models.TextField()


class LTIUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                primary_key=True,
                                on_delete=models.CASCADE)
    tenant = models.ForeignKey(LTITenant)
    last_launch_parameters = JSONField()
    last_launch_time = models.DateTimeField()


