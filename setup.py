import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="p_jwt_validator_adrianlazar-personal",
    version="1.0.0",
    author="Adrian Lazar",
    author_email="adrian.lazar95@outlook.com",
    description="Python JWT Signature Validator - Asymetric Keys - From exponent and modulus",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adrianlazar-personal/py-jwt-validator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)