import json

from django.core.urlresolvers import reverse
from django.test.utils import override_settings
from oauth2_provider.tests.base import BaseTestCase
from provider.constants import PUBLIC


@override_settings(OAUTH2_ALLOW_EDX_SESSION_GRANT=True)
class EdxSessionAccessTokenTestCase(BaseTestCase):

    def setUp(self):
        super(EdxSessionAccessTokenTestCase, self).setUp()
        self.auth_client.client_type = PUBLIC
        self.auth_client.save()
        self.default_params = {
            'grant_type': 'edx_session',
            'scope': 'openid profile',
            'client_id': self.auth_client.client_id,
        }

    def get_access_token_response(self, params=None):
        """
        DRY helper.
        """
        return self.client.post(
            reverse('oauth2:access_token'),
            data=params if params is not None else self.default_params
        )

    @override_settings(OAUTH2_ALLOW_EDX_SESSION_GRANT=False)
    def test_authenticated_user_without_setting(self):
        """
        Ensure the OAUTH2_ALLOW_EDX_SESSION_GRANT setting controls whether or
        not the edx_session grant can be used to obtain tokens.
        """
        self.client.login(username=self.user.username, password=self.password)
        response = self.get_access_token_response()
        self.assertEqual(400, response.status_code)
        self.assertEqual({'error': 'invalid_grant'}, json.loads(response.content))

    def test_authenticated_user(self):
        """
        Ensure a currently-authenticated user can successfully obtain tokens.
        """
        self.client.login(username=self.user.username, password=self.password)
        response = self.get_access_token_response()
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            {'access_token', 'id_token', 'token_type', 'scope', 'expires_in'},
            set(json.loads(response.content).keys())
        )

    def test_anonymous_user(self):
        """
        Ensure a user that is not authenticated cannot obtain tokens.
        """
        self.client.logout()
        response = self.get_access_token_response()
        self.assertEqual(400, response.status_code)
        self.assertEqual({'error': 'invalid_grant'}, json.loads(response.content))

    def test_invalid_client_id(self):
        """
        Ensure that client_id is being checked before issuing tokens.
        """
        self.client.login(username=self.user.username, password=self.password)
        token_request_params = self.default_params.copy()
        token_request_params['client_id'] = 'invalid'
        response = self.get_access_token_response(token_request_params)
        self.assertEqual(400, response.status_code)
        self.assertEqual({'error': 'invalid_client'}, json.loads(response.content))

