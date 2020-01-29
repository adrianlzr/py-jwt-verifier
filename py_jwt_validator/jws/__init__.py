######################################################
# 
#                 JWS
#     
######################################################

import hashlib

class JWS:

    def __init__(self, py_jwt_exception_class, decoded_header, decoded_payload, message, signature, jwk_instance, utils_instance):

        self.py_jwt_exception = py_jwt_exception_class
        self.message = message
        self.signature = signature
        self.jwk = jwk_instance
        self.utils = utils_instance

        self.algorithm = str(decoded_header.get("alg")).lower()
        self.kid = decoded_header.get("kid")
        self.issuer = decoded_payload.get("iss")

        self.verifiers = {
            "rs256": self.RSASSA_PKCS1_V1_5_VERIFY
        }
        self.verifier = self.compute_verifier()(self.py_jwt_exception, self.jwk, self.utils, self.kid, self.issuer, self.message, self.signature)

    def compute_verifier(self):

        verifier = self.verifiers.get(self.algorithm)
        if verifier is None:
            raise PyJwtException("alg")
        return verifier

    class RSASSA_PKCS1_V1_5_VERIFY:

        ######################################################
        # 
        #           RSASSA_PKCS1_V1_5_VERIFY
        #     
        ######################################################

        """
        RFC - JSON Web Signature (JWS) -  RSASSA-PKCS1-V1_5-VERIFY ((n, e), M, S) 
        https://tools.ietf.org/html/rfc3447.html#section-8.2.2 

        HUMAN-READABLE ARTICLE THAT EXPLAINS THIS PROCESS - 
        https://medium.com/@bn121rajesh/rsa-sign-and-verify-using-openssl-behind-the-scene-bf3cac0aade2
        """

        def __init__(self, py_jwt_exception_class, jwk_instance, utils_instance, kid, issuer, message, signature):
            
            self.py_jwt_exception = py_jwt_exception_class
            self.jwk = jwk_instance
            self.utils = utils_instance
            self.kid = kid
            self.issuer = issuer
            self.message = message
            self.signature = signature

        def RSASVP1(self, s, n):

            ## https://tools.ietf.org/html/rfc3447.html#section-5.2.2 
            ## s should be greater than 0 and less than (n-1)
            if s < 0 and s > (n - 1):
                raise JWS.py_jwt_exception("sig") 

        def message_hash(self, message):

            digest = hashlib.sha256()
            digest.update(message)
            digest = digest.hexdigest()
            computed_hash = digest[-40:]
            return computed_hash    

        def signature_hash(self, s, e, n):

            s_hash = hex(pow(s, e, n))
            s_hash = s_hash[-40:]
            return s_hash   

        def verify_signature(self):

            try:
                exponent, modulus = self.jwk.get_e_n(self.kid, self.issuer)
            except UnboundLocalError:
                raise self.py_jwt_exception("no-authz")

            ## Length Checking. len(signature) must equal len(modulus)
            if len(self.signature) != len(modulus):
                raise self.py_jwt_exception("sig")

            ## RSAVP1 verification
            s = self.utils.base64_to_long(self.signature)
            e = self.utils.base64_to_long(exponent)
            n = self.utils.base64_to_long(modulus)
            self.RSASVP1(s, n)

            ## Obtain computed hash of header + . + payload
            computed_hash = self.message_hash(self.message)

            ## Obtain signature hash 
            public_hash = self.signature_hash(s, e, n)

            ## If computed hash does matche signature hash, return True. 
            ## Else, raise Invalid Signature
            if computed_hash == public_hash:
                return None
            raise self.py_jwt_exception("sig")