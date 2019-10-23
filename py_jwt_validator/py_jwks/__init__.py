import requests, requests_cache
from datetime  import timedelta
cache_time = timedelta(days=1)
requests_cache.install_cache(expire_after=cache_time)
requests_cache.remove_expired_responses()

def get_e_n(kid, issuer):
    if 'okta' in issuer:
        if 'oauth2' in issuer:
            url = f"{issuer}/v1/keys"
        else:
            url = f"{issuer}/oauth2/v1/keys"
    elif 'amazonaws' in issuer: ## Added AWS Cognito support.
        url = f"{issuer}/.well-known/jwks.json"
    ## Support for Okta Custom URL domains.
    else:
        if 'oauth2' in issuer:
            url = f"{issuer}/v1/keys"
        else:
            url = f"{issuer}/oauth2/v1/keys"
    try:
        r = requests.get(url)
    except requests.exceptions.SSLError:
        r = requests.get(url, verify=False) ## sometimes the requests lib complains about Okta certificates. Don't know why.
    keys = r.json()['keys']
    for key in keys:
        if kid == key['kid']:
            e = key['e']
            n = key['n']
    return e, n
    