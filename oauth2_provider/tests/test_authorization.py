"""
Tests various flows through using the Authorization Endpoint.
"""
from urlparse import urlparse, parse_qs

import ddt
from provider.oauth2.models import AccessToken
import provider.scope

from oauth2_provider.tests.base import OAuth2TestCase, IDTokenTestCase


@ddt.ddt
class ImplicitFlowTestCase(IDTokenTestCase):
    """
    Test OIDC-related extensions to the OAuth2 Authorization flows
    implemented by this package.
    """

    def _get_auth_payload(self, location):
        """
        DRY helper.  Extract auth parameters from the redirect location as
        returned during the implicit flow.
        """
        self.assertTrue(location.startswith(self.auth_client.redirect_uri + '#'))
        return {k: v[0] for k, v in parse_qs(urlparse(location).fragment).items()}

    def _get_access_token(self, scope):
        """
        DRY helper.  Find the access token generated during our auth request.
        """
        return AccessToken.objects.get(
            user=self.user, client=self.auth_client, scope=provider.scope.to_int(*scope.split())
        )

    @ddt.data(
        ('openid', 'id_token token'),
        ('openid', 'id_token'),
        ('openid profile', 'id_token'),
        ('openid profile email', 'id_token'),
    )
    @ddt.unpack
    def test_oidc_implicit_flow(self, scope, response_type):
        """
        Ensure that valid permutations of scope and response_type result in
        correct OIDC behavior under the implicit flow.
        """
        response = self.login_and_authorize(scope=scope, response_type=response_type, trusted=True)
        self.assertEqual(302, response.status_code)
        auth_payload = self._get_auth_payload(response['Location'])

        # check state
        self.assertEqual(auth_payload['state'], 'some_state')

        # check scope
        self.assertEqual(set(auth_payload['scope'].split()), set(scope.split()))

        # ensure the access token and token type are present or not, based on the response type
        if response_type == 'id_token token':
            expected_token = self._get_access_token(scope)
            self.assertEqual(auth_payload['token_type'], 'Bearer')
            self.assertEqual(auth_payload['access_token'], expected_token.token)
        else:
            self.assertNotIn('token_type', auth_payload)
            self.assertNotIn('access_token', auth_payload)

        # validate the id token
        self.assertValidIDToken(
            auth_payload['id_token'],
            self.auth_client.client_secret,
            audience=self.auth_client.client_id,
        )

    def test_oauth_implicit_flow(self):
        """
        Ensure that standard implicit flow takes effect if response type
        'token' is used without the 'openid' scope.
        """
        response = self.login_and_authorize(scope='profile', response_type='token', trusted=True)
        self.assertEqual(302, response.status_code)
        auth_payload = self._get_auth_payload(response['Location'])

        # check state
        self.assertEqual(auth_payload['state'], 'some_state')

        # check scope
        self.assertEqual(auth_payload['scope'], 'profile')

        expected_token = self._get_access_token('profile')

        self.assertEqual(auth_payload['token_type'], 'Bearer')
        self.assertEqual(auth_payload['access_token'], expected_token.token)

    @ddt.data(
        ('openid', 'token'),  # use of 'token' response type with 'openid' scope is undefined / unsupported
        ('profile', 'id_token'),  # use of 'id_token' response type requires 'openid' scope
        ('profile', 'id_token token'),  # same, even if 'token' is also present
    )
    @ddt.unpack
    def test_implicit_flow_invalid(self, scope, response_type):
        """
        Ensure that invalid permutations of scope and response_type result in
        an oauth error (400).
        """
        response = self.login_and_authorize(scope=scope, response_type=response_type, trusted=True)
        self.assertEqual(400, response.status_code)
