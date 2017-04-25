"""
Custom OAuth2 models

"""

from django.db import models

from provider.oauth2.models import Client

# Import constants to force override of `provider.scope`
# See constants.py for explanation
from . import constants  # pylint: disable=unused-import


class TrustedClient(models.Model):
    """
    By default `django-oauth2-provider` shows a consent form to the
    user after his credentials has been validated. Trusted clients
    bypass the user consent and redirect to the OAuth2 client
    directly.

    """
    client = models.ForeignKey(Client)

    class Meta(object):
        db_table = 'oauth2_provider_trustedclient'


class OidcIssuer(models.Model):
    """
    The OIDC issuer for the related client. According to the OpenID connect
    specification, the url of the OidcIssuer should use the `https` scheme,
    host and optionally the port number and path.
    """
    client = models.ForeignKey(Client, related_name='oidc_issuer')
    url = models.URLField()

    class Meta(object):
        db_table = 'oauth2_provider_oidc_issuer'
