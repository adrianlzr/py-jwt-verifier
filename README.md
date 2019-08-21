# py-jwt-validator
 
JWT Signature Validator, for JWT signed with Asymmetric Keys, public key compiled from exponent and modulus.

----------------
## Disclaimer
Currently, this package is just in beta status. More work is required until it can be considered "production ready".

----------------

## Version:
0.0.1-beta 

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

The class PyJwtValidator currently accepts:
* jwt - only mandatory argument
* cid - OIDC Client ID - optional
* aud - Audience - optional
* iss - Issuer - optional

----------------

## Process Chain
* Once the class is instantiated the following checks are performed:
    * JWT Format
    * JWT Expiration time
    * JWT Claims if given when the class was instantiated.

* After the above checks are done, it will verify the token signature with the public exponent and modulus obtained from the /keys endpoint. If the signature is valid, it will return **None**. Else, it will raise exception.

    * If a check fails at any given step, the exception **PyJwtException** will be raised.
    * The /keys endpoint will be compiled based on the 'iss' claim.
    * The response from /keys will be cached (**requests_cache**) for subsequent calls. Cache lifetime hardcoded to **24 hours**. Cache store is **sqlite**.

* **return_data()** method can be used after all checks are passed. 

----------------

### Note

The reason why this class returns **None** or exception is to provide more flexibility. Not everyone needs to return the decoded payload of the jwt. 

It is recommended to use it within **try:** **except** blocks. 

----------------
# UPCOMING IN FUTURE RELEASES

* Custom Claim validation
* Cache Control (use-case, cache-expiry)
* Return Payload or None

----------------
# SUGGESTIONS?
Please feel free to email me at adrian.lazar95@outlook.com or adrian.lazar@okta.com. I am opened to improvement / suggestions and critics. 