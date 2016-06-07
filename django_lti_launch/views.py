from django.core.urlresolvers import reverse
from django.views.generic import TemplateView

from ltilaunch import LTIUSER_SESSION_KEY
from ltilaunch.models import LTIUser


class SuccessView(TemplateView):
    template_name = "success.html"

    def get_context_data(self, **kwargs):
        context = super(SuccessView, self).get_context_data(**kwargs)
        launch_data = LTIUser.objects.get(
            pk=self.request.session[LTIUSER_SESSION_KEY]).last_launch_parameters
        context['user'] = self.request.user
        context['launch_data'] = launch_data
        context['next_link'] = reverse('return')
        return context
