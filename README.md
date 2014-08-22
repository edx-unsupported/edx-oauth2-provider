edX OAuth2 Provider
===================
OAuth2 provider for edX Platform.

Installation
------------

1. Update `INSTALLED_APPS`:

        INSTALLED_APPS = {
            ...
            'provider',
            'provider.oauth2',
            'oauth2_provider',
        }

2. (Optional) Specify additional data handler. This function will be passed a `User` object. It should return a `dict`
 with any data that should be returned with the access token response. The keys of the return `dict` should not include
 any of the following: access_token, token_type, expires_in, refresh_token, scope. These are reserved for the actual
 access token response and will be ignored if returned.

        # project/app/handlers.py

        def add_user_info(user):
            info = {}
            ...
            return info


        # project/settings.py

        OAUTH2_ADDITIONAL_DATA_HANDLER = 'project.app.handlers.add_user_info'

Testing
-------

        $ ./manage.py test


Usage
-----

The OAuth2 clients must be registered to obtain their `client_id` and `client_secret`. The registration can be done using the
/admin web interface by adding new entries to the OAuth2 Clients table.

Apart from the two basic OAuth2 client types (public and confidential), this provider as a notion of a trusted
client. Trusted client do not require user consent for accessing user resources, and will not show up the approval page
during the sing-in process. To make a client trusted after it has been created, add it to the OAuth2-provider
TrustedModel tables using the /admin web interface.


How to Contribute
-----------------
Contributions are very welcome, but for legal reasons, you must submit a signed
[individual contributor's agreement](http://code.edx.org/individual-contributor-agreement.pdf)
before we can accept your contribution. See our
[CONTRIBUTING](https://github.com/edx/edx-platform/blob/master/CONTRIBUTING.rst)
file for more information -- it also contains guidelines for how to maintain
high code quality, which will make your contribution more likely to be accepted.


Reporting Security Issues
-------------------------
Please do not report security issues in public. Please email security@edx.org.


Mailing List and IRC Channel
----------------------------

You can discuss this code on the [edx-code Google Group](https://groups.google.com/forum/#!forum/edx-code) or in the
`edx-code` IRC channel on Freenode.
