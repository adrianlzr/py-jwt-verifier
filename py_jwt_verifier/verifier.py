from time import time
from typing import Union, Dict

from py_jwt_verifier.jwk import JWK
from py_jwt_verifier.jwt import JWT
from py_jwt_verifier.jws import JWS
from py_jwt_verifier.exceptions import PyJwtException


__all__ = [
    "PyJwtVerifier",
]


class PyJwtVerifier:

    def __init__(
        self,
        jwt: str,
        alg: str = None,
        cid: str = None,
        aud: str = None,
        iss: str = None,
        auto_verify=True,
        check_expiry=True,
        cache_enabled=True,
        cache_lifetime=1,
        cache_store="sqlite",
        oidc_metadata_url=None,
        custom_claims: dict = None,
    ) -> None:
        self.jwt = JWT.from_encoded(jwt)
        if check_expiry:
            self.is_expired()

        self.alg = alg
        self.cid = cid
        self.aud = aud
        self.iss = iss
        if not custom_claims:
            custom_claims = {}
        self.custom_claims = custom_claims

        self.jwk = JWK(
            cache_enabled=cache_enabled,
            cache_lifetime=cache_lifetime,
            cache_store=cache_store,
            oidc_metadata_url=oidc_metadata_url,
        )

        self.jws = JWS(
            jwt=self.jwt,
            jwk=self.jwk,
        )

        if auto_verify is True:
            self.verify()

    def is_expired(self) -> None:
        exp = self.jwt.payload.get("exp")
        if exp:
            time_now = int(time())

            if time_now >= exp:
                raise PyJwtException("exp")

    def verify(self, get_payload=False) -> Union[dict, None]:
        # Validate claims.
        if self.cid:
            if self.cid != self.jwt.payload.get("cid"):
                raise PyJwtException("cid")
        if self.aud:
            if self.aud != self.jwt.payload.get("aud"):
                raise PyJwtException("aud")
        if self.iss:
            if self.iss != self.jwt.payload.get("iss"):
                raise PyJwtException("iss")
        if self.custom_claims:
            if not isinstance(self.custom_claims, dict):
                raise PyJwtException("custom_claims_type")
            # k - claim name, v - claim value
            for k, v in self.custom_claims.items():
                if v != self.jwt.payload.get(k):
                    raise PyJwtException("custom_claim")

        # Validate the signature.
        self.jws.verify_signature()

        # Optional output.
        if get_payload is True:
            return self.return_payload()

    def return_payload(self) -> Dict[str, dict]:
        return {"header": self.jwt.header, "payload": self.jwt.payload}
