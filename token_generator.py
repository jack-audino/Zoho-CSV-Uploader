import traceback, urllib.request, urllib.parse, popup_window, path_translator

'''
Useful links for how Tokens Work:
    Authentication Requests: https://www.zoho.com/crm/developer/docs/api/v2.1/auth-request.html
    Access and Refresh Tokens: https://www.zoho.com/crm/developer/docs/api/v2.1/access-refresh.html
    Using Refresh Tokens: https://www.zoho.com/crm/developer/docs/api/v2.1/refresh.html
    Revoking Refresh Tokens: https://www.zoho.com/crm/developer/docs/api/v2.1/revoke-tokens.html
'''

# reads config.txt and returns a string of the desired item
def read_config(desiredItem: str):
    with open(path_translator.resource_path('config/config.txt'), 'r') as f:
        lineList = f.readlines()
        for i in range(len(lineList)):
            if desiredItem in lineList[i]:
                line = lineList[i].strip('\n').split(' = ')
                if len(line) > 1:
                    return line[1]
                else:
                    return None
        return None

# writes to a given string to an item in config.txt
def write_to_config(stringToWrite: str, itemToChange: str):
    with open(path_translator.resource_path('config/config.txt'), 'r') as f:
        lineList = f.readlines()
        for i in range(len(lineList)):
            if itemToChange in lineList[i]:
                lineList[i] = stringToWrite + '\n'
                break
    
    with open(path_translator.resource_path('config/config.txt'), 'w') as f:
        f.writelines(lineList)

# parses response data for a token type returns the token type
def parse_for_token(givenString: str, tokenType: str):
    givenString = givenString[3 : len(givenString) - 2] # remove the first 3 characters and the last 2 characters since they are always the same
    # the first 3 characters will always be: b'{
    # the last 2 characters will always be: }'
    givenString = givenString.split(',') # cut the line up by each individual item

    for i in range(len(givenString)):
        if tokenType in givenString[i]:
            givenString[i] = givenString[i].split(':') # if the token type is in the current item, split the item 
            token = givenString[i][1] # grab the token
            token = token.replace('"', '') # santize the token by removing quotes
            return tokenType.upper() + ' = ' + token

# uses the Grant Token parsed from config.txt, which creates an Access Token, Refresh Token and Refreshed Access Token
def use_grant_token():
    try:
        url = 'https://accounts.zoho.com/oauth/v2/token'

        grantToken = read_config('GRANT_TOKEN')
        clientID = read_config('CLIENT_ID')
        clientSecret = read_config('CLIENT_SECRET')
                    
        req_params = {
            'code': grantToken,
            'client_id': clientID,
            'client_secret': clientSecret,
            'grant_type':'authorization_code'
        }

        data = urllib.parse.urlencode(req_params)
        data = data.encode('utf-8')

        req = urllib.request.Request(url, data)

        resp = urllib.request.urlopen(req)
        respData = resp.read()

        # if it's empty, then tell the user to add a new Grant Token
        if grantToken is None:
            error = popup_window.popupWindow('There was no Grant Token found.\nAdd a new one in the Edit Config Window.')
            error.display_error()

        # if it's wrong, alert the user that it's wrong and to add a new one
        elif str(respData) == 'b\'{"error":"invalid_code"}\'':
            error = popup_window.popupWindow('Invalid Grant Token Used.\nGenerate a new one in the API console using the scope:\n\"aaaserver.profile.ALL,ZohoCRM.modules.leads.CREATE\"\nand put it into the configuration file.')
            error.display_error()

        # if the client is incorrect, tell the user to add one
        elif str(respData) == 'b\'{"error":"invalid_client"}\'':
            error = popup_window.popupWindow('Invalid Client Information Used.\nEnsure that the client information\nin the configuration file matches\nthe information in the API console.')
            error.display_error()

        elif not str(respData) == 'b\'{"error":"invalid_code"}\'' and not str(respData) == 'b\'{"error":"invalid_client"}\'':
            accessToken = parse_for_token(str(respData), 'access_token')
            refreshToken = parse_for_token(str(respData), 'refresh_token')
            write_to_config(accessToken, 'ACCESS_TOKEN')
            write_to_config(refreshToken, 'REFRESH_TOKEN')
            use_refresh_token()
            popup = popup_window.popupWindow('Grant Token entered successfully.\nAn Access Token, Refresh Token,\nand Refreshed Access Token have\nbeen created.')
            popup.display_popup()
        
    except Exception:
        error = popup_window.popupWindow(traceback.format_exc())
        error.display_error()

# creates a Refreshed Access Token (REFRESHED_ACCESS_TOKEN in config.txt) for the program to use
def use_refresh_token():
    try:
        url = 'https://accounts.zoho.com/oauth/v2/token'

        refreshToken = read_config('REFRESH_TOKEN')
        clientID = read_config('CLIENT_ID')
        clientSecret = read_config('CLIENT_SECRET')
        refreshedAccessToken = read_config('REFRESHED_ACCESS_TOKEN') # used for error message printing

        req_params = {
            'refresh_token':refreshToken,
            'client_id':clientID,
            'client_secret':clientSecret,
            'grant_type':'refresh_token'
        }

        data = urllib.parse.urlencode(req_params)
        data = data.encode('utf-8')

        req = urllib.request.Request(url, data)

        resp = urllib.request.urlopen(req)
        respData = resp.read()

        # if there is no Refresh Token, tell the user
        if str(respData) == 'b\'{"error":"invalid_code"}\'' and refreshToken is None:
                error = popup_window.popupWindow('There was no Refresh Token found.\nCreate a new one by adding a new Grant Token \nin the \'Edit Config\' Window and then hitting the\n\'Use Grant Token\' button in the \'Developer\' Window.')
                error.display_error()

        # if there is one, but it's wrong, tell the user
        elif str(respData) == 'b\'{"error":"invalid_code"}\'' and refreshToken is not None:
            error = popup_window.popupWindow('Invalid Refresh Token Used.\nCreate a new one by adding a new Grant Token \nin the \'Edit Config\' Window and then hitting the\n\'Use Grant Token\' button in the \'Developer\' Window.')
            error.display_error()

        elif not str(respData) == 'b\'{"error":"invalid_code"}\'':
            refreshedAccessToken = parse_for_token(str(respData), 'access_token')
            # rename it to 'REFRESHED_ACCESS_TOKEN' so it's not confused with the original access token
            refreshedAccessToken = refreshedAccessToken.replace('ACCESS_TOKEN', 'REFRESHED_ACCESS_TOKEN')
            write_to_config(refreshedAccessToken, 'REFRESHED_ACCESS_TOKEN')

    except Exception:
        error = popup_window.popupWindow(traceback.format_exc())
        error.display_error()

# sends a revoke request for the current Refresh Token and deletes it (and the Refreshed Access Token, since it will no longer be useable) from config.txt
def revoke_refresh_token():
    try:
        url = 'https://accounts.zoho.com/oauth/v2/token/revoke'

        refreshTokenToDelete = read_config('REFRESH_TOKEN')

        if refreshTokenToDelete is not None:
            req_params = {
                'token':refreshTokenToDelete
            }

            data = urllib.parse.urlencode(req_params)
            data = data.encode('utf-8')

            req = urllib.request.Request(url, data)

            try: 
                resp = urllib.request.urlopen(req) 
                # if req is invalid or empty, it can't send the request to a non-existent webpage, so a timeout error occurs and crashes the program, it must be caught by an exception
                respData = resp.read()
                print(str(respData))

                # if it is successful, then remove the Refresh Token and Refreshed Access Token from the config
                if 'success' in str(respData):
                    write_to_config('REFRESH_TOKEN =', 'REFRESH_TOKEN')
                    write_to_config('REFRESHED_ACCESS_TOKEN =', 'REFRESHED_ACCESS_TOKEN')
                    popup = popup_window.popupWindow('Refresh Token and Refreshed Access Token revoked successfully.')
                    popup.display_popup()

            except Exception:
                print(str(respData))
                # if it's incorrect, then alert the use to create a new one
                error = popup_window.popupWindow('Invalid Refresh Token.\nIt is either incorrect or has already been revoked.\nCreate a new one by adding a new Grant Token \nin the \'Edit Config\' Window and then hitting the\n\'Use Grant Token\' button in the \'Developer\' Window.')
                error.display_error()
        else:
            error = popup_window.popupWindow('There was no Refresh Token found.\nCreate a new one by adding a new Grant Token \nin the \'Edit Config\' Window and then hitting the\n\'Use Grant Token\' button in the \'Developer\' Window.')
            error.display_error()
        
    except Exception:
        error = popup_window.popupWindow(traceback.format_exc())
        error.display_error()

# wipes config.txt
def wipe_config():
    with open(path_translator.resource_path('config/config.txt'), 'w') as f:
        f.write('GRANT_TOKEN =\n' +
                'ACCESS_TOKEN =\n' +
                'REFRESH_TOKEN =\n' +
                'REFRESHED_ACCESS_TOKEN =\n' +
                'HOME_DIRECTORY =\n' +
                'CLIENT_ID =\n' +
                'CLIENT_SECRET =')