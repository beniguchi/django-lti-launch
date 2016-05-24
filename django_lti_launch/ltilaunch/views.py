import logging

from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

logger = logging.getLogger(__name__)


class LaunchView(View):
    success_redirect_url = '/'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(LaunchView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        return HttpResponseRedirect(resolve_url(self.success_redirect_url),
                                    status=303)
