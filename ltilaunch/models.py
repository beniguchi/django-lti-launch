import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField, ArrayField
from django.db import models
from django.utils import timezone

from .utils import generate_random_string


logger = logging.getLogger(__name__)


class LTIToolConsumer(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    oauth_consumer_key = models.TextField(
        unique=True,
        default=generate_random_string,
        verbose_name="OAuth consumer key")
    oauth_consumer_secret = models.TextField(
        default=generate_random_string,
        verbose_name="OAuth consumer secret")
    tool_consumer_instance_guid = models.TextField(
        verbose_name="Tool consumer instance GUID")
    match_guid_and_consumer = models.BooleanField(
        default=True,
        verbose_name="Match GUID and OAuth consumer")
    recent_nonces = ArrayField(base_field=models.TextField(),
                               size=10, default=[])

    def __str__(self):
        return self.name

    def add_nonce(self, nonce):
        self.recent_nonces = [nonce] + self.recent_nonces[:9]
        self.save()

    class Meta:
        verbose_name = "LTI tool consumer"


class LTIUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True,
                                on_delete=models.CASCADE)
    lti_tool_consumer = models.ForeignKey(LTIToolConsumer)
    lti_user_id = models.TextField()
    last_launch_parameters = JSONField()
    last_launch_time = models.DateTimeField()

    class Meta:
        unique_together = ('lti_tool_consumer', 'lti_user_id')


class LTIToolProvider(models.Model):
    name = models.SlugField(blank=False, unique=True)
    description = models.TextField()
    icon_url = models.URLField(blank=True)
    launch_path = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "LTI tool provider"


def get_or_create_lti_user(consumer, lti_user_id, request):
    try:
        lti_user = LTIUser.objects.get(
            lti_tool_consumer=consumer,
            lti_user_id=lti_user_id)
        lti_user.last_launch_parameters = request.POST
        lti_user.last_launch_time = timezone.now()
    except LTIUser.DoesNotExist:
        user_model = get_user_model()
        djuser = user_model.objects.create_user(
            username=(consumer.tool_consumer_instance_guid[:14] +
                      lti_user_id[:14]))
        lti_user = LTIUser.objects.create(
            user=djuser,
            lti_user_id=lti_user_id,
            lti_tool_consumer=consumer,
            last_launch_parameters=request.POST,
            last_launch_time=timezone.now()
        )
    lti_user.save()
    return lti_user


def lti_launch_return_url(user):
    result = None
    try:
        lti_user = LTIUser.objects.get(user=user)
    except LTIUser.DoesNotExist:
        logger.error("no LTIUser found for '%s'", user)
    else:
        result = lti_user.last_launch_parameters.get(
            'launch_presentation_return_url', None)
    return result
