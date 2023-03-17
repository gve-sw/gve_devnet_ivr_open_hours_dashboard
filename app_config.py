import os

b2c_tenant = os.getenv('TENANT_NAME')
signin_user_flow = os.getenv('SIGNIN_USER_FLOW')

authority_template = "https://{tenant}.b2clogin.com/{tenant}.onmicrosoft.com/{user_flow}"

# Application (client) ID of app registration
CLIENT_ID = os.getenv("CLIENT_ID")
# Application's generated client secret: never check this into source control!
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

AUTHORITY = authority_template.format(tenant=b2c_tenant, user_flow=signin_user_flow)

REDIRECT_PATH = "/getAToken"  # Used for forming an absolute URL to your redirect URI.
# The absolute URL must match the redirect URI you set
# in the app's registration in the Azure portal.

# These are the scopes you've exposed in the web API app registration in the Azure portal
SCOPE = []

SESSION_TYPE = "filesystem"  # Specifies the token cache should be stored in server-side session
