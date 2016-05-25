import json

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField, ArrayField
from django.db import models
from django.utils import timezone


class LTIToolConsumer(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    oauth_consumer_key = models.TextField(unique=True)
    oauth_consumer_secret = models.TextField()
    tool_consumer_instance_guid = models.TextField()
    recent_nonces = ArrayField(base_field=models.TextField(),
                               size=10, default=[])

    def add_nonce(self, nonce):
        self.recent_nonces = [nonce] + self.recent_nonces[:9]
        self.save()


class LTIUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                primary_key=True,
                                on_delete=models.CASCADE)
    lti_tool_consumer = models.ForeignKey(LTIToolConsumer)
    lti_user_id = models.TextField()
    last_launch_parameters = JSONField()
    last_launch_time = models.DateTimeField()

    class Meta:
        unique_together = ('lti_tool_consumer', 'lti_user_id')


def get_consumer_for_oauth_consumer_key(consumer_key):
    try:
        return LTIToolConsumer.objects.get(oauth_consumer_key=consumer_key)
    except LTIToolConsumer.DoesNotExist:
        return None


def get_or_create_lti_user(consumer, lti_user_id, request):
    try:
        lti_user = LTIUser.objects.get(
            lti_tool_consumer=consumer,
            lti_user_id=lti_user_id)
        lti_user.last_launch_parameters = json.dumps(request.POST)
        lti_user.last_launch_time = timezone.now()
    except LTIUser.DoesNotExist:
        user_model = get_user_model()
        djuser = user_model.objects.create_user(
            username=consumer.tool_consumer_instance_guid[:14] + lti_user_id[:14])
        lti_user = LTIUser.objects.create(
            user=djuser,
            lti_user_id=lti_user_id,
            lti_tool_consumer=consumer,
            last_launch_parameters=json.dumps(request.POST),
            last_launch_time=timezone.now()
        )
    lti_user.save()
    return lti_user
