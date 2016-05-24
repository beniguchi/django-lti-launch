import datetime
import json

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField, ArrayField
from django.db import models


class LTIToolConsumer(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    oauth_consumer_key = models.TextField(unique=True)
    oauth_consumer_secret = models.TextField()
    tool_consumer_instance_guid = models.TextField(primary_key=True)
    recent_nonces = ArrayField(base_field=models.TextField(),
                               size=10, default=[])

    def add_nonce(self, nonce):
        self.recent_nonces = [nonce] + self.recent_nonces[:9]
        self.save()


class LTIUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                primary_key=True,
                                on_delete=models.CASCADE)
    tool_consumer_instance_guid = models.ForeignKey(LTIToolConsumer)
    lti_user_id = models.TextField()
    last_launch_parameters = JSONField()
    last_launch_time = models.DateTimeField()

    class Meta:
        unique_together = ('tool_consumer_instance_guid', 'lti_user_id')


def lti_user_for_request(request):
    consumer_guid = request.POST['tool_consumer_instance_guid']
    user_id = request.POST['user_id']
    try:
        lti_user = LTIUser.objects.get(
            tool_consumer_instance_guid=consumer_guid,
            lti_user_id=user_id)
        lti_user.last_launch_parameters = json.dumps(request.POST)
        lti_user.last_launch_time = datetime.now()
        lti_user.save()
    except LTIUser.DoesNotExist:
        user_model = get_user_model()
        djuser = user_model.create_user(
            username=consumer_guid[:14] + user_id[:14])
        lti_user = LTIUser.objects.create(
            user=djuser,
            tool_consumer_instance_guid=consumer_guid,
            last_launch_parameters=json.dumps(request.POST),
            last_launch_time=datetime.now()
        )
        lti_user.save()
    return lti_user
