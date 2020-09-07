import Twitter_Utils as APPMODULES

user ,user_firstname, user_lastanme ,user_email = APPMODULES.userInfo()

if user is None:

    response, content = APPMODULES.requestTokenClient()
    Token = APPMODULES.requestTokenCallback(response, content)
    access_token_callback = APPMODULES.accessToken(token=Token)
    user = APPMODULES.saving_New_to_DB(access_token_callback, user_firstname, user_lastanme, user_email)

authorized_client = APPMODULES.getAuthorizationToken(user, user_email)
APPMODULES.searchAPI(authorized_client)