from django.core.urlresolvers import reverse
from django.views.generic import TemplateView

from ltilaunch.models import LTIUser


class SuccessView(TemplateView):
    template_name = "success.html"

    def get_context_data(self, **kwargs):
        context = super(SuccessView, self).get_context_data(**kwargs)
        launch_data = LTIUser.objects.get(
            user=self.request.user).last_launch_parameters
        context['launch_data'] = launch_data
        context['next_link'] = reverse('return')
        return context
