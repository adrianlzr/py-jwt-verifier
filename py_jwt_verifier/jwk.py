from datetime import timedelta
from json.decoder import JSONDecodeError
from typing import Union, Tuple, Literal

from requests import Session
from requests_cache import (
    CachedSession,
    BaseCache,
    FileCache,
    SQLiteCache,
    RedisCache,
    MongoCache,
    GridFSCache,
    DynamoDbCache,
)
from requests.exceptions import SSLError

from py_jwt_verifier.exceptions import PyJwtException

PY_JWT_CACHE_NAME = "pyw-jwt-verifier"
PY_JWT_DEFAULT_CACHE_STORE = "sqlite"

__all__ = ["JWK"]


class JWK:
    def __init__(
        self,
        cache_enabled: bool = True,
        cache_store: Union[
            Literal[
                "memory",
                "filesystem",
                "sqlite",
                "redis",
                "mongodb",
                "gridfs",
                "dynamodb",
            ],
            BaseCache,
            FileCache,
            SQLiteCache,
            RedisCache,
            MongoCache,
            GridFSCache,
            DynamoDbCache,
        ] = PY_JWT_DEFAULT_CACHE_STORE,
        cache_lifetime: int = 1,
        oidc_metadata_url: Union[str, None] = None,
    ) -> None:
        if cache_lifetime > 30 or cache_lifetime < 1:
            raise PyJwtException("cache-lifetime")
        self.oidc_metadata_url = oidc_metadata_url

        if cache_enabled:
            try:
                self._session = CachedSession(
                    cache_name=PY_JWT_CACHE_NAME,
                    backend=cache_store,
                    expire_after=cache_lifetime,
                )
            except ValueError:
                raise PyJwtException("cache-store")
        else:
            self._session = Session()

    def get_e_n(self, issuer: str, kid: Union[str, None] = None) -> Tuple[str, str]:
        if kid:
            return self._get_e_n_with_kid(issuer, kid)
        return self._get_e_n(issuer)

    def _get_e_n_with_kid(self, issuer: str, kid: str) -> Tuple[str, str]:
        keys_endpoint = self._compute_keys_endpoint(issuer)
        keys = self._get_json_response(keys_endpoint).get("keys", [])
        for key in keys:
            if key.get("kid") == kid:
                return key.get("e"), key.get("n")
        raise PyJwtException("kid")

    def _get_e_n(self, _: str) -> Tuple[str, str]:
        raise NotImplementedError("Not yet suupported.")

    def _compute_keys_endpoint(self, issuer) -> str:
        metadata_url = self.oidc_metadata_url

        if metadata_url is None:
            metadata_url = f"{issuer}/.well-known/openid-configuration"

        # Some issuers end with a trailing "/".
        # Auth0 is one of the idps that set the issuer as such.
        if "//." in metadata_url:
            metadata_url = f"{issuer}.well-known/openid-configuration"

        metadata = self._get_json_response(metadata_url)
        return metadata.get("jwks_uri")

    def _get_json_response(self, url) -> dict:
        try:
            return self._session.get(url).json()
        except SSLError:
            raise PyJwtException("ssl")
        except JSONDecodeError:
            raise PyJwtException("json")
