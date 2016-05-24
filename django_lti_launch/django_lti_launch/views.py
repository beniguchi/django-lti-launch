from ltilaunch.views import LaunchView


class TestLaunchView(LaunchView):
    success_redirect_url = '/succeeded'

    def post(self, request):
        resp = super(TestLaunchView, self).post(request)
        resp.content = "workaround"  # avoids django SSL server error spam
                                     # see https://git.io/vrKJM
                                     # unneeded outside of testing
        return resp
