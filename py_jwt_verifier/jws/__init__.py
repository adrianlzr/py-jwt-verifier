from py_jwt_verifier.exceptions import PyJwtException
from py_jwt_verifier.jws.base import JWSVerifier
from py_jwt_verifier.jws.rs256 import RSASSA_PKCS1_V1_5_VERIFY
from py_jwt_verifier.jwk import JWK
from py_jwt_verifier.jwt import JWT


__all__ = ["JWS"]


PY_JWT_ALG_RS256 = "rs256"


def _create_signature_verifier(jwt: JWT, jwk: JWK) -> JWSVerifier:
    alg = str(jwt.header.get("alg")).lower()
    if alg == PY_JWT_ALG_RS256:
        return RSASSA_PKCS1_V1_5_VERIFY(jwt, jwk)
    raise PyJwtException("alg")


class JWS:

    def __init__(self, jwt: JWT, jwk: JWK) -> None:
        self._verifier = _create_signature_verifier(jwt, jwk)

    def verify_signature(self):
        self._verifier.verify_signature()
