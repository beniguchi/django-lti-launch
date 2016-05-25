import oauthlib.oauth1
from django.core.urlresolvers import reverse
from django.test import TestCase, override_settings

from ltilaunch.models import LTIToolConsumer, LTIUser


@override_settings(ROOT_URLCONF='ltilaunch.test_urls',
                   AUTHENTICATION_BACKENDS=('ltilaunch.auth.LTILaunchBackend',))
class LaunchViewTestCase(TestCase):
    key = "oauthconsumerkey123456826387216487264821641"
    secret = "oauthconsumersecret1234536821638126382136183"
    guid = "abcdefg"
    user_id = "user1"

    def setUp(self):
        self.consumer = LTIToolConsumer.objects.create(
            name="testconsumer",
            description="Test LTI Tool Consumer",
            oauth_consumer_key=self.key,
            oauth_consumer_secret=self.secret,
            tool_consumer_instance_guid=self.guid
        )
        self.uri = "https://testserver" + reverse("testlaunch")

    def test_wrong_consumer(self):
        oauth_signer = oauthlib.oauth1.Client(
            client_key="invalid",
            client_secret=self.secret,
            signature_type=oauthlib.oauth1.SIGNATURE_TYPE_BODY)
        params = {"tool_consumer_instance_guid": self.guid,
                  "user_id": self.user_id}
        uri, headers, body = oauth_signer.sign(
            self.uri,
            http_method="POST",
            body=params,
            headers={"Content-Type":"application/x-www-form-urlencoded" })
        resp = self.client.post(uri, body, headers=headers,
                                secure=True,
                                content_type="application/x-www-form-urlencoded")
        self.assertIsNotNone(resp, "response should not be None")
        self.assertEquals(401, resp.status_code,
                          "response status should be 401 Unauthorized")
        self.assertNotIn('sessionid', resp.client.cookies)

    def test_success(self):
        oauth_signer = oauthlib.oauth1.Client(
            client_key=self.key,
            client_secret=self.secret,
            signature_type = oauthlib.oauth1.SIGNATURE_TYPE_BODY)
        params = {"tool_consumer_instance_guid": self.guid,
                  "user_id": self.user_id}
        uri, headers, body = oauth_signer.sign(
            self.uri,
            http_method="POST",
            body=params,
            headers={"Content-Type":"application/x-www-form-urlencoded" })
        resp = self.client.post(uri, body, headers=headers,
                                secure=True,
                                content_type="application/x-www-form-urlencoded")
        self.assertIsNotNone(resp, "response should not be None")
        users = LTIUser.objects.filter(lti_user_id=self.user_id)
        self.assertEqual(1, len(users), "user should exist")
        self.assertRedirects(resp, '/', status_code=303,
                             fetch_redirect_response=False)
        self.assertIn('sessionid', resp.client.cookies)


