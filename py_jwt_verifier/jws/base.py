__all__ = [
    "JWSVerifier",
]


class JWSVerifier:
    """
    Provide skeleton for JWS Verifier implementations.
    """

    def verify_signature(self):
        raise NotImplementedError("All sub-classes must implement this method.")
