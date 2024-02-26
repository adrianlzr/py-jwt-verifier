__all__ = [
    "PY_JWT_ERRORS",
    "PY_JWT_DEFAULT_ERROR",
    "PyJwtException",
]


PY_JWT_ERRORS = {
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
    "json": "Invalid JSON data. Either the /keys endpoint is not reachable or the response data is invalid.",
}

PY_JWT_DEFAULT_ERROR = "General, non-determined error."


class PyJwtException(Exception):
    def __init__(self, arg: str = None) -> None:
        super().__init__(PY_JWT_ERRORS.get(arg, PY_JWT_DEFAULT_ERROR))
