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
jwt = {access_token / id_token}
validator = PyJwtValidator(jwt, auto_verify=False)
try:
    payload = validator.verify(True)
    print(payload)
except PyJwtException as e:
    print(f"Exception caught. Error: {e}")
```

**Using cache control:**

* redis

```
from redis import StrictRedis
from py_jwt_validator import PyJwtValidator, PyJwtException


redis = StrictRedis(host="localhost", port=6390)

jwt = 'eyJraWQiOiIzZ3p2akJhTU9oaC01enRiRFRrb0tPd1BFTXVCY24wOHhUSkpaQ1lVRGQ4IiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiIwMHVrcWlkMHF1WWJ1WDg2ajBoNyIsIm5hbWUiOiJBZHJpYW4gTGF6xINyIiwiZW1haWwiOiJsenIuYWRyaWFuOTVAZ21haWwuY29tIiwidmVyIjoxLCJpc3MiOiJodHRwczovL2Fkcmlhbi5va3RhcHJldmlldy5jb20iLCJhdWQiOiIwb2FsdGFxNzYyTDBtOEtBUzBoNyIsImlhdCI6MTU4MDI4MTE2MiwiZXhwIjoxNTgwMjg0NzYyLCJqdGkiOiJJRC5oM3VMelFweGd1dkFWcXNwOXo4YXpiTUxKbmpxQzFYX1VfN0JTQ3dCN2hBIiwiYW1yIjpbInB3ZCJdLCJpZHAiOiIwMG9pYW41eDBkb2FFeEpXMDBoNyIsInByZWZlcnJlZF91c2VybmFtZSI6ImFkcmlhbi5sYXphckBhZHJpYW4tbGF6YXIuY29tIiwiYXV0aF90aW1lIjoxNTgwMjgxMTYyLCJhdF9oYXNoIjoiQTZNZkRZaDB6bU5haXRsM1R6dGszQSJ9.BTNUYXbHsXds469I45HsE7YddfMXFZGMusNVFRAz0IO7uB3244LBGIgKajCcDGgBRFZH9W10gy3YPMlXQPoGskqFROkr3NS-Ovy6_V7g-DG_zlZhb1QJulqUX6OmuVjypUPiB-sfl3poSXF4L4LEaPEgRo_y_O3CR6VEX6Fu84U_nX2HRso8OJMfXYC4eWf_mYUVshvklcj7TprbqMnNeB4fghi8_bAISw2FcX-A3_2E28PyFQfiRZvwODcIQkZUJITteR427vDSUdoUkb2ma3xrvLvYxX6Mem1b8RgRf3MS41s1fOOS6MO_LmGFD_3Gy4Qy0mH6gl-_-TVc6MBDng'
try:
    print(PyJwtValidator(jwt, auto_verify=False, check_expiry=False, cache_store="redis", cache_store_connection=redis).verify(True))
except PyJwtException as e:
    print(f"Exception caught. Error: {e}")
```

* PyMongo

```
from pymongo import MongoClient
from py_jwt_validator import PyJwtValidator, PyJwtException


mongo = MongoClient("localhost", 27017)

jwt = 'eyJraWQiOiIzZ3p2akJhTU9oaC01enRiRFRrb0tPd1BFTXVCY24wOHhUSkpaQ1lVRGQ4IiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiIwMHVrcWlkMHF1WWJ1WDg2ajBoNyIsIm5hbWUiOiJBZHJpYW4gTGF6xINyIiwiZW1haWwiOiJsenIuYWRyaWFuOTVAZ21haWwuY29tIiwidmVyIjoxLCJpc3MiOiJodHRwczovL2Fkcmlhbi5va3RhcHJldmlldy5jb20iLCJhdWQiOiIwb2FsdGFxNzYyTDBtOEtBUzBoNyIsImlhdCI6MTU4MDI4MTE2MiwiZXhwIjoxNTgwMjg0NzYyLCJqdGkiOiJJRC5oM3VMelFweGd1dkFWcXNwOXo4YXpiTUxKbmpxQzFYX1VfN0JTQ3dCN2hBIiwiYW1yIjpbInB3ZCJdLCJpZHAiOiIwMG9pYW41eDBkb2FFeEpXMDBoNyIsInByZWZlcnJlZF91c2VybmFtZSI6ImFkcmlhbi5sYXphckBhZHJpYW4tbGF6YXIuY29tIiwiYXV0aF90aW1lIjoxNTgwMjgxMTYyLCJhdF9oYXNoIjoiQTZNZkRZaDB6bU5haXRsM1R6dGszQSJ9.BTNUYXbHsXds469I45HsE7YddfMXFZGMusNVFRAz0IO7uB3244LBGIgKajCcDGgBRFZH9W10gy3YPMlXQPoGskqFROkr3NS-Ovy6_V7g-DG_zlZhb1QJulqUX6OmuVjypUPiB-sfl3poSXF4L4LEaPEgRo_y_O3CR6VEX6Fu84U_nX2HRso8OJMfXYC4eWf_mYUVshvklcj7TprbqMnNeB4fghi8_bAISw2FcX-A3_2E28PyFQfiRZvwODcIQkZUJITteR427vDSUdoUkb2ma3xrvLvYxX6Mem1b8RgRf3MS41s1fOOS6MO_LmGFD_3Gy4Qy0mH6gl-_-TVc6MBDng'
try:
    print(PyJwtValidator(jwt, auto_verify=False, check_expiry=False, cache_store="mongo", cache_store_connection=mongo).verify(True))
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