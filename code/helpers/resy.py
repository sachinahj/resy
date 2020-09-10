import helpers.datetime
import helpers.logger

import json
import requests

log = helpers.logger.Logger(__name__)


API_KEY = 'VbWk7s3L4KiK5fzlO7JD3Q5EYolJI7n5'
USER = None

def write(filename, data):
    with open(f"./scratch/{filename}.json", 'w') as f:
        json.dump(data, f)

def _headers(headers):
    return { **{
        'Authorization': f"ResyAPI api_key=\"{API_KEY}\"",
    }, **headers }

def _get(url, params={}, headers={}):
    headers = _headers(headers)
    r = requests.get(url, headers=headers, params=params)
    return json.loads(r.content)

def _post(url, data={}, headers={}):
    headers = _headers(headers)
    r = requests.post(url, headers=headers, data=data)
    log.info("_post", request_headers=r.request.headers)
    response = json.loads(r.content)
    return response

def login(email, password):
    global USER
    data = {
        'email': email,
        'password': password,
    }
    response = _post("https://api.resy.com/3/auth/password", data)
    write('user', response)
    USER = response

def find(date, venue_id, party_size):
    params = {
        'day': helpers.datetime.date_resy(date),
        'venue_id': venue_id,
        'party_size': party_size,
        'lat': 0,
        'long': 0,
    }
    response = _get(f"https://api.resy.com/4/find", params)
    write('find', response)
    return response['results']['venues']

def details(config_token, date, party_size):
    params = {
        'config_id': config_token,
        'day': helpers.datetime.date_resy(date),
        'party_size': party_size,
    }
    response = _get(f"https://api.resy.com/3/details", params)
    write('details', response)
    return response

def book(book_token):
    data = {
        'book_token': book_token,
    }
    headers = {
        'x-resy-auth-token': USER['token']
    }
    response = _post("https://api.resy.com/3/book", data, headers)
    return response
