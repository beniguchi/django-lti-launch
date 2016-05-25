import logging

from django.contrib.auth import get_user_model

from ltilaunch.models import get_or_create_lti_user, get_consumer_for_oauth_consumer_key
from ltilaunch.oauth import validate_lti_launch

logger = logging.getLogger(__name__)


class LTILaunchBackend:
    required_keys = {'oauth_consumer_key',
                     'user_id',
                     'tool_consumer_instance_guid'}

    def authenticate(self, launch_request=None):
        result = None
        if launch_request:
            if launch_request.POST.keys() & self.required_keys:
                consumer_key = launch_request.POST['oauth_consumer_key']
                lti_user_id = launch_request.POST['user_id']
                consumer = get_consumer_for_oauth_consumer_key(consumer_key)
                if not consumer:
                    logger.error(
                        "no LTI consumer found for OAuth consumer key '%s'",
                        consumer_key)
                else:
                    is_valid, _ = validate_lti_launch(
                        consumer,
                        launch_request.build_absolute_uri(),
                        launch_request.body,
                        launch_request.META)
                    if not is_valid:
                        logger.error(
                            "LTI launch not valid for OAuth consumer key %s, user_id %s",
                            consumer_key, lti_user_id)
                    else:
                        lti_user = get_or_create_lti_user(
                            consumer, lti_user_id, launch_request)
                        result = lti_user.user
        return result

    def get_user(self, user_id):
        um = get_user_model()
        try:
            return um.objects.get(pk=user_id)
        except um.DoesNotExist:
            return None
