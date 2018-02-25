import requests
import sys

login = sys.argv[2]
right = sys.argv[3]
fundation = sys.argv[1]

headers = {
    'Host': 'api.nemopay.net',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
    'Accept': 'application/json',
    'Accept-Language': 'fr-FR',
    'Referer': 'https://admin.nemopay.net/',
    'Content-Type': 'application/json',
    'Origin': 'https://admin.nemopay.net',
    'Connection': 'keep-alive',
}

params = (
    ('system_id', 'payutc'),
    ('app_key', '0a93e8e18e6ed78fa50c4d74e949801b'),
    ('sessionid', '2v7ubhv0m44pufp742rd4n51all0el4g'),
)

data = '{"queryString":"'+str(login)+'","wallet_config":1}'

response = requests.post('https://api.nemopay.net/services/GESUSERS/walletAutocomplete', headers=headers, params=params, data=data)
print(response.json()[0]['id'])

newid = response.json()[0]['id']

headers = {
    'Accept': 'application/json, text/plain, /',
    'Accept-Language': 'fr-FR',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Host': 'api.nemopay.net',
    'Nemopay-Version': '2017-12-15',
    'Origin': 'https://admin.nemopay.net',
    'Referer': 'https://admin.nemopay.net/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
}

params = (
    ('sessionid', '2v7ubhv0m44pufp742rd4n51all0el4g'),
    ('system_id', 'payutc'),
)

data = '{"obj":'+str(newid)+',"fundation":'+str(fundation)+',"location":null,"event":1,"name":"'+str(right)+'"}'
#response = requests.delete('https://api.nemopay.net/resources/walletrights/256', headers=headers, params=params)

#data = '{"id":256,"obj":5964,"location":null,"fundation":45,"name":"SALES",
#"event":1,"created":"2018-02-23T16:23:30.924194Z",
#"removed":null,"wallet":{"id":5964,
#"name":"Compte par d\xE9faut","user":{
#"id":15482,"first_name":"Axel","last_name":
#"DUPART","email":"axel.dupart@etu.utc.fr","username":"dupartax",
#"photo_url":"","organisation":"","phone":""}}}'
response = requests.post('https://api.nemopay.net/resources/walletrights', headers=headers, params=params, data=data)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.post('https://api.nemopay.net/services/GESUSERS/walletAutocomplete?system_id=payutc&app_key=0a93e8e18e6ed78fa50c4d74e949801b&sessionid=2v7ubhv0m44pufp742rd4n51all0el4g', headers=headers, data=data)
#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.post('https://api.nemopay.net/services/GESUSERS/walletAutocomplete?system_id=payutc&app_key=0a93e8e18e6ed78fa50c4d74e949801b&sessionid=2v7ubhv0m44pufp742rd4n51all0el4g', headers=headers, data=data)


#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.post('https://api.nemopay.net/resources/walletrights?sessionid=2v7ubhv0m44pufp742rd4n51all0el4g&system_id=payutc', headers=headers, data=data)
