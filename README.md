# py-jwt-validator
 
JWT Signature Validator, for JWT signed with Asymmetric Keys, public key compiled from exponent and modulus.

----------------

## Install
```
pip install py-jwt-validator
```

----------------

## Get Started
```
from py_jwt_validator import PyJwtValidator
jwt = {access_token / id_token}
_jwt = PyJwtValidator(jwt)
print(_jwt.return_data())
```

The class PyJwtValidator currently accepts:
* jwt - only mandatory argument
* cid - OIDC Client ID - optional
* aud - Audience - optional
* iss - Issuer - optional

----------------

## Process Chain
* As soon as the class is instantiated, it performs the following:
    * Checks if the jwt format is valid. If invalid, it will return exception: InvalidJwtFormat.
    * Checks if the jwt is expired. If expired, it will return exception: JwtExpired.
    * If any of the above claims are passed, it will decode the payload, and check if the claims are present as passed. If there will be no match, it will return exception: InvalidClaim.
    * After the above checks are done, it will verify the token signature with the public exponent and modulus obtained from issuer/v1/keys. If the signature is valid, it will return **None**. Else, it will raise exception: InvalidSignature.
        * Note: if oauth2/{authServerId} is not present in the issuer, it will send the request directly to oauth2/v1/keys.
* If no exception will be returned, the return_data() method is accesible and can be used to return the decoded payload of the jwt. 

----------------

### Note

The reason why this class returns **None** or exception is to provide more flexibility. Not everyone needs to return the decoded payload of the jwt. 

It is recommended to use it within **try:** **except** blocks. 

