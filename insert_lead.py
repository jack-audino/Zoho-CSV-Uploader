import urllib.request, urllib.parse, json, token_generator, traceback, popup_window

# Reference API page: https://www.zoho.com/crm/developer/docs/api/v2/insert-records.html

# Example of a properly-formatted record_list:
'''
    record_list = [
        {
            'Last_Name':'User 1',
            'First_Name':'Test',
            'Designation':'Addition #1',
            'Email':'testuser1@tce.org',
            'Company':'Test Company Enterprises',
            'Phone':'1111111111'
        },
        {
            'Last_Name':'User 2',
            'First_Name':'Test',
            'Designation':'Addition #2',
            'Email':'testuser2@tce.org',
            'Company':'Test Company Enterprises',
            'Phone':'2222222222'
        }
    ]
'''

# creates a new access token by using the refresh token, and then uses it to upload the parsed data
def send_parsed(parsedData: list()):
    newAccessToken = token_generator.read_config('REFRESHED_ACCESS_TOKEN')
    try:
        newAccessToken = 'Zoho-oauthtoken ' + newAccessToken # have to add 'Zoho-oauthtoken ' at the beginning, otherwise the request will not be correctly-formatted
        url = 'https://www.zohoapis.com/crm/v2/Leads'

        headers = {
            'Authorization': newAccessToken
        }

        request_body = dict()
        record_list = parsedData

        request_body['data'] = record_list

        trigger = [
            'approval',
            'workflow',
            'blueprint'
        ]

        request_body['trigger'] = trigger

        data = json.dumps(request_body)
        data = data.encode('utf-8')

        req = urllib.request.Request(url, data, headers = headers)
        
        resp = urllib.request.urlopen(req)
        respData = resp.read()

        return str(respData)

    except Exception:
        if newAccessToken is None:
            error = popup_window.popupWindow('No Refreshed Access Token found.\nCreate a new Refresh Token and Refreshed Access\nToken by adding a new Grant Token in the\n\'Edit Config\' Window and then hitting the\n\'Use Grant Token\' button in the \'Developer\' Window.')
            error.display_error()
        elif newAccessToken is not None:
            error = popup_window.popupWindow('Invalid Refreshed Access Token used.\nCreate a new Refresh Token and Refreshed Access\nToken by adding a new Grant Token in the\n\'Edit Config\' Window and then hitting the\n\'Use Grant Token\' button in the \'Developer\' Window.')
            error.display_error()
        else:
            error = popup_window.popupWindow(traceback.format_exc())
            error.display_error()