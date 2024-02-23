######################################################
# 
#                 PyJwtException
#     
######################################################

class PyJwtException(Exception):
    def __init__(self, arg=None):
        self.params = {
            "alg": "Unsupported algorithm. Supported algorithms: RS256.",
            "len": "JWT length is invalid.",
            "exp": "JWT is expired.",
            "cid": "Invalid Client ID present in the payload.",
            "aud": "Invalid Audience present in the payload.",
            "iss": "Invalid Issuer present in the payload.",
            "custom_claim": "The specified Custom Claim/s does not seem to be valid/exist.",
            "custom_claims_type": "The **custom_claims object must be of type dict!",
            "sig": "JWT Signature is not valid.",
            "kid": """Unable to find a matching kid. Please invalidate the cache as the keys might've been rotated. If the issue persists 
            the JWT is either invalid or in case of Okta: Access Tokens can only be validated locally if they were issued by a Custom Authorization Server.""",
            "ssl": "The SSL Certificate seems to be issued for a different domain or the certificate chain is not present.",
            "cache-store": "Invalid cache store. Please choose between: memory, sqlite, mongo and redis.",
            "cache-lifetime": "Invalid cache lifetime! The lifetime must be higher than 1 and less than 30 days.",
            "json": "Invalid JSON data. Either the /keys endpoint is not reachable or the response data is invalid."
        }
        if arg not in self.params:
            Exception.__init__(self, "General, non-determined error.")

        for k, v in self.params.items():
            if k == arg:
                Exception.__init__(self, f'{v}')


######################################################
# 
#                 PyJwtVerifier
#     
######################################################

from time import time

from .jwk import JWK
from .jws import JWS
from .utils import Utils


class PyJwtVerifier:

    def __init__(self, jwt, 
                 cid=None, aud=None, iss=None, auto_verify=True, check_expiry=True,
                 cache_enabled=True, cache_lifetime=1, cache_store="sqlite",
                 cache_store_connection=None, oidc_metadata_url=None, **custom_claims):

        self.jwt = jwt.split(".")
        self.is_format_valid()

        self.header = self.jwt[0]
        self.payload = self.jwt[1]
        self.signature = self.jwt[2]
        self.message = self.header.encode("ascii") + b"." + self.payload.encode("ascii") ## will be used to obtain the computed hash

        self.utils = Utils()
        self.decoded_jwt = self.utils.b64_decode(self.jwt)
        self.decoded_header = self.decoded_jwt[0]
        self.decoded_payload = self.decoded_jwt[1]
        
        if check_expiry:
            self.is_expired()

        self.cid = cid
        self.aud = aud
        self.iss = iss
        self.custom_claims = custom_claims
        
        self.jwk = JWK(PyJwtException, cache_enabled, cache_lifetime, cache_store, cache_store_connection, oidc_metadata_url)
        self.jws = JWS(PyJwtException, self.decoded_header, self.decoded_payload, self.message, self.signature, self.jwk, self.utils)
        
        if auto_verify is True:
            self.verify()

    def is_format_valid(self):

        if len(self.jwt) < 3 or len(self.jwt) > 3:
            raise PyJwtException("len")

    def is_expired(self):
        # expiry claim is optional
        exp = self.decoded_payload.get("exp")
        if exp:
            time_now = int(time())
            
            if time_now >= exp:
                raise PyJwtException("exp")

    def verify(self, get_payload=False):


        ### CLAIM VALIDATION. 
        if self.cid:
            if self.cid != self.decoded_payload.get("cid"):
               raise PyJwtException("cid")
        if self.aud:
            if self.aud != self.decoded_payload.get("aud"):
                raise PyJwtException("aud")
        if self.iss:
            if self.iss != self.decoded_payload.get("iss"):
                raise PyJwtException("iss")
        if self.custom_claims:
            if not isinstance(self.custom_claims, dict):
                raise PyJwtException("custom_claims_type")
            for k, v in self.custom_claims.items(): # k - claim name, v - claim value
                if v != self.decoded_payload.get(k):
                    raise PyJwtException("custom_claim")

        ### SIGNATURE VALIDATION
        self.jws.verifier.verify_signature()           

        ### OUTPUT
        if get_payload is True:
            return self.return_payload()

    def return_payload(self):

        return {
            "header":self.decoded_header,
            "payload":self.decoded_payload
        }
