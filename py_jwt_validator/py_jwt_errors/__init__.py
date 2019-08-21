class PyJwtException:
    
    class InvalidJwtFormat(Exception):
        def __init__(self):
            Exception.__init__(self, "Invalid JWT! Format is not recognized.")

    class JwtExpired(Exception):        
        def __init__(self):
            Exception.__init__(self, "JWT Expired!")

    class InvalidSignature(Exception):        
        def __init__(self):
            Exception.__init__(self, "Invalid Signature!")

    class InvalidClaim(Exception):        
        def __init__(self, arg):
            Exception.__init__(self, f"Invalid Claim! {arg} does not match the expected {arg}.")