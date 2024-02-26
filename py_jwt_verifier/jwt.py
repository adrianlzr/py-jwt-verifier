from typing import Union, List, Dict, Any

from py_jwt_verifier.exceptions import PyJwtException
from py_jwt_verifier import utils


__all__ = ["JWT"]

PY_JWT_SEPARATOR = "."
PY_JWT_EXPECTED_LEN = 3
PY_JWT_HEADER_IDX = 0
PY_JWT_PAYLOAD_IDX = 1
PY_JWT_SIGNATURE_IDX = 2


class JWT:

    __slots__ = (
        "encoded",
        "decoded",
        "header",
        "payload",
        "message",
        "signature",
    )

    @classmethod
    def from_encoded(cls, encoded: str) -> "JWT":
        encoded_split = encoded.split(PY_JWT_SEPARATOR)
        # Ensure the format is valid by checking that splitting the
        # encoded str by "." will result in a list with len == {PY_JWT_EXPECTED_LEN}.
        # Will raise PyJwtException("len") when lentgth isn't the exepcted one.
        if len(encoded_split) != PY_JWT_EXPECTED_LEN:
            raise PyJwtException("len")

        # Set the header, payload, message and signature.
        decoded = utils.b64_decode(encoded_split)
        header, payload = (
            decoded[PY_JWT_HEADER_IDX],
            decoded[PY_JWT_PAYLOAD_IDX],
        )
        message = (
            encoded_split[PY_JWT_HEADER_IDX].encode("ascii")
            + PY_JWT_SEPARATOR.encode("ascii")
            + encoded_split[PY_JWT_PAYLOAD_IDX].encode("ascii")
        )
        signature = encoded_split[PY_JWT_SIGNATURE_IDX]

        return JWT(
            encoded=encoded,
            decoded=decoded,
            header=header,
            payload=payload,
            message=message,
            signature=signature,
        )

    def __init__(
        self,
        encoded: str,
        decoded: List[Dict[str, Any]],
        header: Dict[str, Any],
        payload: Dict[str, Any],
        message: bytes,
        signature: str,
    ) -> None:
        self.encoded = encoded
        self.decoded = decoded
        self.header = header
        self.payload = payload
        self.message = message
        self.signature = signature
