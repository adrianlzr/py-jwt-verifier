import requests, requests_cache
from datetime  import timedelta
cache_time = timedelta(days=1)
requests_cache.install_cache(expire_after=cache_time)
requests_cache.remove_expired_responses()

def get_e_n(kid, issuer):
    if 'oauth2' in issuer:
        url = f"{issuer}/v1/keys"
    else:
        url = f"{issuer}/oauth2/v1/keys"

    r = requests.get(url)
    keys = r.json()['keys']
    for key in keys:
        if kid == key['kid']:
            e = key['e']
            n = key['n']
    return e, n
    