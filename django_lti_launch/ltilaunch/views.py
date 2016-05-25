from django.contrib.auth import login, authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import resolve_url
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View


class LaunchView(View):
    success_redirect_url = '/'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(LaunchView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        lti_user = authenticate(launch_request=request)
        if lti_user:
            login(request, lti_user)
            return HttpResponseRedirect(resolve_url(self.success_redirect_url),
                                        status=303)
        else:
            unauthorized = HttpResponse(status=401)
            unauthorized['WWW-Authenticate'] = 'OAuth realm=""'
            return unauthorized
