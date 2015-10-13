"""
OAuth2 provider `django-oauth2-provider` authentication backends

"""
from oauth2_provider.forms import PublicPasswordGrantForm, EdxSessionGrantForm


class PublicClientIdFormBackend(object):
    """
    Generic client authentication wrapper backend that delegates to a form
    class which extracts a public Client instance based on the client_id
    parameter.
    """
    form_class = None  # override in subclasses.

    def authenticate(self, request=None):
        """ Returns client if correctly authenticated. Otherwise returns None """

        if request is None:
            return None

        form = self.form_class(request.REQUEST)

        # pylint: disable=no-member
        if form.is_valid():
            return form.cleaned_data.get('client')

        return None


class PublicPasswordBackend(PublicClientIdFormBackend):
    """
    Provides Client extraction via client_id for the password grant.
    """
    form_class = PublicPasswordGrantForm


class ExistingSessionBackend(PublicClientIdFormBackend):
    """
    Provides Client extraction via client_id for the edx_session grant.
    """
    form_class = EdxSessionGrantForm
