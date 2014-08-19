# Use bit-shifting so that scopes can be easily combined and checked.
DEFAULT_SCOPE = 0
USERNAME_SCOPE = 1

# Define OAuth scopes. Required by django-oauth2-provider.
# The default scope value is OAUTH_SCOPES[0][0]
SCOPES = (
    (DEFAULT_SCOPE, 'default'),
    (USERNAME_SCOPE, 'preferred_username'),
)
