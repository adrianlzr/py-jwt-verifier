import time
from .py_jwt_errors import PyJwtException
from .py_jwt_b64 import b64_decode
from .py_jwks import get_e_n
from .py_jwt_signature import verify_signature

invalid_format = PyJwtException.InvalidJwtFormat
jwt_expired = PyJwtException.JwtExpired
invalid_claim = PyJwtException.InvalidClaim

class PyJwtValidator:
    def __init__(self, jwt, cid=None, aud=None, iss=None):
        self.jwt = jwt.split('.')
        self.is_format_valid()
        self.decoded_jwt = b64_decode(self.jwt)
        self.header = self.jwt[0]
        self.payload = self.jwt[1]
        self.signature = self.jwt[2]
        self.decoded_header = self.decoded_jwt[0]
        self.decoded_payload = self.decoded_jwt[1]
        self.is_expired()
        self.cid = cid
        self.aud = aud
        self.iss = iss
        self.verify()
    ##Initial Checks
    def is_format_valid(self):
        if len(self.jwt) < 3 or len(self.jwt) >3:
            raise invalid_format
    def is_expired(self):
        time_now = int(time.time())
        exp = self.decoded_payload['exp']
        if time_now >= exp:
            raise jwt_expired
    def verify(self):
        if self.cid:
            if self.cid != self.decoded_payload['cid']:
               raise invalid_claim('Client ID')
        if self.aud:
            if self.aud != self.decoded_payload['aud']:
                raise invalid_claim('Audience')
        if self.iss:
            if self.iss != self.decoded_payload['iss']:
                raise invalid_claim('Issuer')
        e, n = get_e_n(self.decoded_header['kid'], self.decoded_payload['iss'])
        message = self.header.encode('ascii') + b'.' + self.payload.encode('ascii')
        signature = self.signature
        is_valid = verify_signature(signature, message, e, n) 
    def return_data(self):
        return self.decoded_payload