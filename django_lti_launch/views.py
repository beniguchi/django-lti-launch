from ltilaunch.views import LaunchView


class TestLaunchView(LaunchView):

    def post(self, request):
        resp = super(TestLaunchView, self).post(request)
        # non-empty resp.content avoids django SSL server error spam
        # see https://git.io/vrKJM, unneeded outside of testing
        resp.content = "workaround"
        return resp
