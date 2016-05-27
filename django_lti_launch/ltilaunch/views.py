from urllib.parse import urlparse, urlunparse

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from ltilaunch.models import lti_launch_return_url


class LaunchView(View):
    tool_provider_url = '/'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(LaunchView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        result = HttpResponse(status=401)
        result['WWW-Authenticate'] = 'OAuth realm=""'
        lti_user = authenticate(launch_request=request)
        if lti_user:
            login(request, lti_user)
            result = HttpResponseRedirect(self.tool_provider_url, status=303)
        return result


class ReturnRedirectView(View):
    @method_decorator(login_required)
    def get(self, request):
        # FIXME: not sure what best default behavior is
        result = HttpResponseNotFound()
        return_url = lti_launch_return_url(request.user)
        if return_url:
            parsed = urlparse(return_url)
            new_q = request.GET.urlencode()
            if parsed.query != '':
                new_q = new_q + "&" + parsed.query
            url = urlunparse(
                (parsed[0],
                 parsed[1],
                 parsed[2],
                 parsed[3],
                 new_q,
                 parsed[5]))
            result = HttpResponseRedirect(url, status=303)
        return result
