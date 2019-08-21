import hashlib
from py_jwt_validator import PyJwtException
from py_jwt_validator.py_jwt_b64 import base64_to_long

def RSASVP1(s, n):
    ## https://tools.ietf.org/html/rfc3447.html#section-5.2.2 
    ## s should be greater than 0 and less than (n-1)
    if s < 0 and s > (n -1):
        raise PyJwtException('sig')

def message_hash(message):
    digest = hashlib.sha256()
    digest.update(message)
    digest = digest.hexdigest()
    computed_hash = digest[-40:]
    return computed_hash

def signature_hash(s, e, n):
    s_hash = hex(pow(s, e, n))
    s_hash = s_hash[-40:]
    return s_hash

def verify_signature(signature, message, exponent, modulus):
    ## RFC Method of validating JSON Web Signature (JWS) -  RSASSA-PKCS1-V1_5-VERIFY ((n, e), M, S) https://tools.ietf.org/html/rfc3447.html#section-8.2.2 
    ## HUMAN-READABLE ARTICLE THAT EXPLAINS THIS PROCESS - https://medium.com/@bn121rajesh/rsa-sign-and-verify-using-openssl-behind-the-scene-bf3cac0aade2
    ## 1. Length Checking. len(signature) must equal len(modulus)
    if len(signature) != len(modulus):
        raise PyJwtException('sig')
    ## RSAVP1 verification
    s = base64_to_long(signature)
    e = base64_to_long(exponent)
    n = base64_to_long(modulus)
    RSASVP1(s, n)
    ## Obtain computed hash of header + . + payload
    computed_hash = message_hash(message)
    ## Obtain signature hash 
    public_hash = signature_hash(s, e, n)
    ## If computed hash does matche signature hash, return True. 
    ## Else, raise Invalid Signature
    if computed_hash == public_hash:
        return None
    raise PyJwtException('sig')