import json
import re
from urllib.parse import urlencode

import bs4
import requests


s = requests.Session()


BASE_URL = "http://connect.garmin.com/en-US/signin"
GAUTH = "https://connect.garmin.com/gauth/hostname"
SSO = "https://sso.garmin.com/sso"
CSS = "https://static.garmincdn.com/com.garmin.connect/ui/css/gauth-custom-v1.2-min.css"
REDIRECT = "https://connect.garmin.com/post-auth/login"
ACTIVITIES = "http://connect.garmin.com/proxy/activity-search-service-1.2/json/activities?start=%s&limit=%s"

response = s.get(BASE_URL)
pattern = "\"\S+sso\.garmin\.com\S+\""
script_url = re.search(pattern, response.content.decode()).group()[1:-1]
s.get(script_url)
s.headers.update({'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.121 Safari/535.2'})
response = s.get(GAUTH)
hostname = json.loads(response.content)['host']
data = {'service': REDIRECT,
    'webhost': hostname,
    'source': BASE_URL,
    'redirectAfterAccountLoginUrl': REDIRECT,
    'redirectAfterAccountCreationUrl': REDIRECT,
    'gauthHost': SSO,
    'locale': 'en_US',
    'id': 'gauth-widget',
    'cssUrl': CSS,
    'clientId': 'GarminConnect',
    'rememberMeShown': 'true',
    'rememberMeChecked': 'false',
    'createAccountShown': 'true',
    'openCreateAccount': 'false',
    'usernameShown': 'false',
    'displayNameShown': 'false',
    'consumeServiceTicket': 'false',
    'initialFocus': 'true',
    'embedWidget': 'false',
    'generateExtraServiceTicket': 'false',
}
login_url = 'https://sso.garmin.com/sso/login?%s' % urlencode(data)
s.get(login_url)
response = s.get(login_url)
soup = bs4.BeautifulSoup(response.content, 'html.parser')
payload = {r['name']: r.get('value', True) for r in soup.find('form').findAll('input')}
payload.update({'username': USERNAME, 'password': PASSWORD})
response = s.post('https://sso.garmin.com' + soup.find('form').attrs['action'], data=payload)
'Invalid' in response.content.decode()
'SUCCESS' in response.content.decode()
response_url = re.search("response_url\s*=\s*'(.*)';", response.content.decode()).groups()[0]
response_url = response_url.replace("\/", "/")
s.get(response_url)
r = s.get('https://connect.garmin.com/modern/proxy/usersummary-service/usersummary/list/rixxtr?start=1&limit=10&maxDate=2017-03-31')
