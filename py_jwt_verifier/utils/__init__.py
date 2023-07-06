######################################################
# 
#                 UTILS
#     
######################################################

from base64 import b64decode, urlsafe_b64decode
from json import loads, dumps
import struct
import six


class Utils:

    def compute_padding(self, part):
        _padding = "=" * (4 - len(part) % 4)
        return _padding

    def b64_decode(self, jwt):
        _jwt = jwt[0:2] #Removing signature [2]
        decoded_jwt = []
        for part in _jwt:
            part = part.replace('_', '/')
            part = part.replace('-', '+')
            part += self.compute_padding(part)
            decoded_jwt.append(loads(b64decode(part)))
        return decoded_jwt

    def intarr2long(self, arr):
        return int(''.join(["%02x" % byte for byte in arr]), 16)

    def base64_to_long(self, data):
        if isinstance(data, six.text_type):
            data = data.encode("ascii")
        # urlsafe_b64decode will happily convert b64encoded data
        _d = urlsafe_b64decode(bytes(data) + b'==')
        return self.intarr2long(struct.unpack('%sB' % len(_d), _d))