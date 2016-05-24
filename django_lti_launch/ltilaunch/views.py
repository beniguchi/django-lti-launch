from django.contrib.auth import login
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import resolve_url
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from ltilaunch.models import LTIToolConsumer, lti_user_for_request
from ltilaunch.oauth import validate_lti_launch


class LaunchView(View):
    success_redirect_url = '/'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(LaunchView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        try:
            consumer_key = request.POST['oauth_consumer_key']
            consumer = LTIToolConsumer.objects.get(
                oauth_consumer_key=consumer_key)
            result = validate_lti_launch(consumer,
                                         request.build_absolute_uri(),
                                         request.body,
                                         request.META)
            if result:
                login(request, lti_user_for_request(request))
                return HttpResponseRedirect(resolve_url(self.success_redirect_url),
                                            status=303)
            else:
                return HttpResponseForbidden("invalid OAuth signed request")
        except LTIToolConsumer.DoesNotExist:
            return HttpResponseForbidden("invalid OAuth consumer key")
