# py-jwt-validator
----------------


## Realease notes
Version | Release notes
------------ | -------------
0.5.0      | **MAJOR Release.** Production stable. Added cache control.
0.4.0-beta | Security fix. Certificate Chain is mandatory for Okta Custom URL Domain.
0.3.0-beta | Minor release. Added support for Okta Custom URL Domain.
0.2.0-beta | Minor release. Added support for AWS Cognito JWT.
0.1.0-beta | Minor release. Increased configurability.
0.0.1-beta | First package release.

----------------


## Supported IdPs
* Okta
* AWS Cognito
* *More to come*

----------------


## Supported Signing Algorithms
* RS256

----------------


## Disclaimer
This library is provded as is. None of the listed IdPs will provide support for issues related with the present library. I am the sole maintainer of it.

----------------


## Process Chain
1. Once the class is instantiated the following checks are performed:
    * JWT Format.
    * JWT Expiration time.
    * JWT Claims if given when the class was instantiated.
    * Is Algorithm Supported.

2. After the above checks are done, it will verify the token signature with the apropriate signing algorithm based on the "alg" header claim. If the signature is valid, it will return **None**. Else, it will raise a exception.

    * If a check fails at any given step, the exception **PyJwtException** will be raised.
    * The /.well-knwon/openid-configuration endoint will be compiled based on the 'iss' claim.
    * The /keys endpoint will be determined from the output of the /.well-knwon/openid-configuration endpoint
    * The response from /keys will be cached (**requests_cache**) for subsequent calls.
    
----------------


## Installation
```
pip install py-jwt-validator
```

----------------


## Usage Examples
```
from py_jwt_validator import PyJwtValidator, PyJwtException
jwt = {access_token / id_token}
try:
    PyJwtValidator(jwt)
except PyJwtException as e:
    print(f"Exception caught. Error: {e}")
```

* If **auto_verify** is set to **False** the class will not perform the signature validation. To check the signature the **verify()** method needs to be used. By default, the method will return None. In order to return the decoded jwt data (header + payload) **True** has to be passed. Example:
```
from py_jwt_validator import PyJwtValidator, PyJwtException
jwt = access_token / id_token
validator = PyJwtValidator(jwt, auto_verify=False)
try:
    payload = validator.verify(True)
    print(payload)
except PyJwtException as e:
    print(f"Exception caught. Error: {e}")
```

**Custom Claim Validation:**

```
from py_jwt_validator import PyJwtValidator, PyJwtException
jwt = access_token / id_token
validator = PyJwtValidator(jwt, auto_verify=False, custom_claim_name="custom_claim_value")
try:
    payload = validator.verify(True)
    print(payload)
except PyJwtException as e:
    print(f"Exception caught. Error: {e}")
```


**Cache Control:**

* redis

```
from redis import StrictRedis
from py_jwt_validator import PyJwtValidator, PyJwtException


redis = StrictRedis(host="localhost", port=6390)

jwt = access_token / id_token
validator = PyJwtValidator(jwt, auto_verify=False, cache_store="redis", cache_store_connection=redis)
try:
    payload = validator.verify(True)
    print(payload)
except PyJwtException as e:
    print(f"Exception caught. Error: {e}")
```

* pymongo

```
from pymongo import MongoClient
from py_jwt_validator import PyJwtValidator, PyJwtException


mongo = MongoClient("localhost", 27017)

jwt = access_token / id_token
validator = PyJwtValidator(jwt, auto_verify=False, cache_store="mongo", cache_store_connection=mongo)
try:
    payload = validator.verify(True)
    print(payload)
except PyJwtException as e:
    print(f"Exception caught. Error: {e}")
```

----------------


## Class Attributes
* The class **PyJwtValidator** currently accepts:

Attribute | Required | Default value
----------|----------|--------------
jwt | Yes | **None**
cid - OIDC Client ID | No | **None**
aud - Audience | No | **None**
iss - Issuer | No | **None**
auto_verify | No | **True**
check_expiry | No | **True**
cache_enabled | No | **True**
cache_lifetime | No | **1 day**
cache_store | No | **sqlite**
cache_store_connection | No | **None**

* The class method **verify()** currently accepts:

Attribute | Required | Default value
----------|----------|--------------
get_payload | No | **False**

## Note

The reason why this class returns **None** or exception is to provide more flexibility. Not everyone needs to return the decoded payload of the jwt. 
It is recommended to use it within **try:** **except** blocks.
 
----------------


## Cache Control
This library relies on the **requests** and **requests_cache** libraries. The caching control mechanism was implemented around these libraries. 


### Cache Control attributes explained
* cache_enabled - Attribute type: Boolean - Accepted Values: True / False. Determines if the cache control mechanism will be used. If set to False, the response from the /.well-knwon/openid-configuration and /keys endpoints will never be cached. 
* cache_lifetime - Attribute type: Integer - Accepted Values: 1 - 30. Represents the number of *days* the cache will be stored and used. The maximum value can not be higher than 30 days or less than 1 day.
* cache_store - Attribute type: String - Accepted Values: "memory", "sqlite", "mongo", "redis". Determines how and where the **requests_cache** library will store the responses and connect to the caching store. When there is no cache_store_connection provided, it will rely on the defaults for mongo and redis.
* cache_store_connection - Attribute type: DB instance object - Should be used only when the cache_store is set to "mongo" or "redis". This is necessary for production environments so you can specify the host, port, database, user and password to use to connect to the respective caching database selected.

### Note
When using redis or mongo as caching database solutions, the appropriate python connector libraries will be required (pymongo / redis).
For additional information in regards of how **requests_cache** works, please review their docs: https://requests-cache.readthedocs.io/en/latest/

----------------


## UPCOMING

- [ ] - HMAC256 support
- [ ] - Additional OIDC IdPs (Google, Facebook, Microsoft, Auth0) 

----------------


## SUGGESTIONS?

Please feel free to email me at adrian.lazar95@outlook.com or lzr.adrian95@gmail.com. I am opened to improvement / suggestions and critics. 