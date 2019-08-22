class PyJwtException(Exception):
    def __init__(self, arg=None):
        self.params = {
            'len': 'JWT length is invalid.',
            'exp':'JWT is expired.',
            'cid':'Invalid Client ID present in the payload.',
            'aud':'Invalid Audience present in the payload',
            'iss':'Invalid Issuer present in the payload',
            'sig':'JWT Signature is not valid.',
            'no-authz':'Okta-Specific: Access Tokens can not be validated locally without a Custom Authorization Server'
        }
        if arg not in self.params:
            Exception.__init__(self, 'General, non-determined error. Oups?')

        for k, v in self.params.items():
            if k == arg:
                Exception.__init__(self, f'{v}')

import time
from .py_jwt_b64 import b64_decode
from .py_jwks import get_e_n
from .py_jwt_signature import verify_signature

class PyJwtValidator:
    def __init__(self, jwt, cid=None, aud=None, iss=None, check_expiry=True, auto_verify=True):
        self.jwt = jwt.split('.')
        self.is_format_valid()
        self.decoded_jwt = b64_decode(self.jwt)
        self.header = self.jwt[0]
        self.payload = self.jwt[1]
        self.signature = self.jwt[2]
        self.decoded_header = self.decoded_jwt[0]
        self.decoded_payload = self.decoded_jwt[1]
        if check_expiry:
            self.is_expired()
        self.cid = cid
        self.aud = aud
        self.iss = iss
        if auto_verify is True:
            self.verify()

    def is_format_valid(self):
        if len(self.jwt) < 3 or len(self.jwt) >3:
            raise PyJwtException('len')

    def is_expired(self):
        time_now = int(time.time())
        exp = self.decoded_payload['exp']
        if time_now >= exp:
            raise PyJwtException('exp')

    def verify(self, get_payload=False):
        if self.cid:
            if self.cid != self.decoded_payload['cid']:
               raise PyJwtException('cid')
        if self.aud:
            if self.aud != self.decoded_payload['aud']:
                raise PyJwtException('aud')
        if self.iss:
            if self.iss != self.decoded_payload['iss']:
                raise PyJwtException('iss')
        try:
            e, n = get_e_n(self.decoded_header['kid'], self.decoded_payload['iss'])
        except UnboundLocalError:
            raise PyJwtException('no-authz')
        message = self.header.encode('ascii') + b'.' + self.payload.encode('ascii')
        verify_signature(self.signature, message, e, n)
        if get_payload is True:
            return self.return_data()
    def return_data(self):
        return self.decoded_payload