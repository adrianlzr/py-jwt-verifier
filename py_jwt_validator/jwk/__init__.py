######################################################
# 
#                 JWK
#     
######################################################

import requests
import requests_cache
from requests.exceptions import SSLError
from datetime  import timedelta
from json.decoder import JSONDecodeError

class JWK:

    def __init__(self, py_jwt_exception_class, cache_enabled, cache_lifetime, cache_store, cache_store_connection):
        
        self.py_jwt_exception = py_jwt_exception_class
        self.cache_enabled = cache_enabled
        if cache_lifetime > 30 or cache_lifetime < 1:
            raise self.py_jwt_exception("cache-lifetime")
        self.cache_lifetime = timedelta(days=cache_lifetime)
        self.cache_store = cache_store
        if cache_enabled:
            try:
                requests_cache.install_cache(expire_after=self.cache_lifetime, backend=self.cache_store, connection=cache_store_connection)   
                requests_cache.remove_expired_responses()
            except ValueError:
                raise PyJwtException("cache-store")

    def get_json_response(self, url):
        try:
            response = requests.get(url)
        except SSLError:
            raise PyJwtException("ssl")
        json_response = response.json()
        return json_response
    
    def compute_keys_endpoint(self, issuer):

        metadata_url = f"{issuer}/.well-known/openid-configuration"
        if "//." in metadata_url: ## some issuers end with a trailing "/". Auth0 is one of the idps that set the issuer as such.
            metadata_url = f"{issuer}.well-known/openid-configuration"
        metadata = self.get_json_response(metadata_url)
        return metadata.get("jwks_uri")
        

    def get_e_n(self, kid, issuer):

        keys_endpoint = self.compute_keys_endpoint(issuer)
        r = requests.get(keys_endpoint)
        keys = r.json().get("keys")
        for key in keys:
            if kid == key.get("kid"):
                e = key.get("e")
                n = key.get("n")
        return e, n