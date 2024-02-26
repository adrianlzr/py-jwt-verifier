import hashlib

from py_jwt_verifier.exceptions import PyJwtException
from py_jwt_verifier.jwk import JWK
from py_jwt_verifier.jwt import JWT
from py_jwt_verifier.jws.base import JWSVerifier
from py_jwt_verifier.utils import base64_to_long


__all__ = ["RSASSA_PKCS1_V1_5_VERIFY"]


class RSASSA_PKCS1_V1_5_VERIFY(JWSVerifier):
    """
    RFC - JSON Web Signature (JWS) -  RSASSA-PKCS1-V1_5-VERIFY ((n, e), M, S)
    https://tools.ietf.org/html/rfc3447.html#section-8.2.2

    HUMAN-READABLE ARTICLE THAT EXPLAINS THIS PROCESS -
    https://medium.com/@bn121rajesh/rsa-sign-and-verify-using-openssl-behind-the-scene-bf3cac0aade2
    """

    def __init__(self, jwt: JWT, jwk: JWK) -> None:
        self.jwt = jwt
        self.jwk = jwk

    def verify_signature(self) -> None:
        iss, kid = self.jwt.payload.get("iss"), self.jwt.header.get("kid")
        exponent, modulus = self.jwk.get_e_n(iss, kid)
        # Length Checking. len(signature) must equal len(modulus)
        if len(self.jwt.signature) != len(modulus):
            raise PyJwtException("sig")

        # RSAVP1 verification
        s = base64_to_long(self.jwt.signature)
        e = base64_to_long(exponent)
        n = base64_to_long(modulus)
        self._RSASVP1(s, n)

        # Obtain computed hash of header + . + payload
        computed_hash = self._message_hash(self.jwt.message)

        # Obtain signature hash
        public_hash = self._signature_hash(s, e, n)

        if computed_hash != public_hash:
            raise PyJwtException("sig")

    def _RSASVP1(self, s, n) -> None:
        """
        https://tools.ietf.org/html/rfc3447.html#section-5.2.2
        s should be greater than 0 and less than (n-1)
        """
        if s < 0 and s > (n - 1):
            raise PyJwtException("sig")

    def _message_hash(self, message) -> str:
        digest = hashlib.sha256()
        digest.update(message)
        digest = digest.hexdigest()
        return digest[-40:]

    def _signature_hash(self, s: int, e: int, n: int) -> str:
        s_hash = hex(pow(s, e, n))
        return s_hash[-40:]
