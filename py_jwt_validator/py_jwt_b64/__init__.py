import base64, json, struct, six

def compute_padding(part):
    _padding = "=" * (4 - len(part) % 4)
    return _padding

def b64_decode(jwt):
    _jwt = jwt[0:2] #Removing signature [2]
    decoded_jwt = []
    for part in _jwt:
        part += compute_padding(part)
        decoded_jwt.append(json.loads(base64.b64decode(part)))
    return decoded_jwt

def intarr2long(arr):
    return int(''.join(["%02x" % byte for byte in arr]), 16)

def base64_to_long(data):
    if isinstance(data, six.text_type):
        data = data.encode("ascii")
    # urlsafe_b64decode will happily convert b64encoded data
    _d = base64.urlsafe_b64decode(bytes(data) + b'==')
    return intarr2long(struct.unpack('%sB' % len(_d), _d))