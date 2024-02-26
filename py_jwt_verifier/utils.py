from base64 import b64decode, urlsafe_b64decode
from json import loads
from struct import unpack
from typing import Tuple, List, Dict


__all__ = ["b64_decode"]


def b64_decode(jwt: List[str]) -> List[Dict[str, dict]]:
    """
    :param jwt: JWT string split into a list of exactly 3 strings.
    :returns: List of 2 dicts: [{header}, {payload}]
    """
    # Removing signature [2]
    decoded_jwt = []
    for part in jwt[0:2]:
        part = part.replace("_", "/")
        part = part.replace("-", "+")
        # Add padding
        part += "=" * (4 - len(part) % 4)
        decoded_jwt.append(loads(b64decode(part)))
    return decoded_jwt


def _int_arr2_long(arr: Tuple[int]) -> int:
    return int("".join(["%02x" % byte for byte in arr]), 16)


def base64_to_long(data) -> int:
    if isinstance(data, str):
        data = data.encode("ascii")
    _d = urlsafe_b64decode(bytes(data) + b"==")
    return _int_arr2_long(unpack("%sB" % len(_d), _d))
