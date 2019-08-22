# py-jwt-validator
 
JWT Signature Validator, for JWT signed with Asymmetric Keys, public key compiled from exponent and modulus.

----------------
## Disclaimer
Currently, this package is just in beta status. More work is required until it can be considered "production ready".

----------------

## Realease notes:
Version | Release notes
------------ | -------------
0.1.0-beta | Minor release. Attributes: Class: check_expiry, auto_verify and Method(**verify()**):get_payload are now available.
0.0.1-beta | First package release.

----------------

## Install
```
pip install py-jwt-validator
```

----------------

## Usage Guide
```
from py_jwt_validator import PyJwtValidator, PyJwtException
jwt = {access_token / id_token}
try:
    _jwt = PyJwtValidator(jwt)
except PyJwtException:
    print('Exception was catched.')
```

The class **PyJwtValidator** currently accepts:

Attribute | Required | Default value
----------|----------|--------------
jwt | Yes | None
cid - OIDC Client ID | No | None
aud - Audience | No | None
iss - Issuer | No | None
auto_verify | No | **True**
check_expiry | No | **True**

The class method **verify(**) currently accepts:

Attribute | Required | Default value
----------|----------|--------------
get_payload | No | **False**

----------------

## Process Chain
1. Once the class is instantiated the following checks are performed:
    * JWT Format
    * JWT Expiration time
    * JWT Claims if given when the class was instantiated.

2. After the above checks are done, it will verify the token signature with the public exponent and modulus obtained from the /keys endpoint. If the signature is valid, it will return **None**. Else, it will raise exception.

    * If a check fails at any given step, the exception **PyJwtException** will be raised.
    * The /keys endpoint will be compiled based on the 'iss' claim.
    * The response from /keys will be cached (**requests_cache**) for subsequent calls. Cache lifetime hardcoded to **24 hours**. Cache store is **sqlite**.

* If **auto_verify** is set to **False** the class will not perform the signature validation. To check the signature the **verify()** method needs to be used. By default, the method will return None. In order to return the decoded jwt payload **True** has to be passed. Example:
```
from py_jwt_validator import PyJwtValidator, PyJwtException
jwt = {access_token / id_token}
validator = PyJwtValidator(jwt, auto_verify=False)
try:
    payload = validator.verify(True)
    print(payload)
except PyJwtException:
    print('Exception was catched.')
```

----------------

### Note

The reason why this class returns **None** or exception is to provide more flexibility. Not everyone needs to return the decoded payload of the jwt. 

It is recommended to use it within **try:** **except** blocks. 

----------------
# UPCOMING IN FUTURE RELEASES

- [x] Disable auto signature verify - **auto_verify=False**
- [x] Return Payload or None - **get_payload=True**
- [x] Ommit expiry check - **check_expiry=False**
- [] Custom Claim validation
- [] Cache Control (use-case, cache-expiry)


----------------
# SUGGESTIONS?
Please feel free to email me at adrian.lazar95@outlook.com or adrian.lazar@okta.com. I am opened to improvement / suggestions and critics. 