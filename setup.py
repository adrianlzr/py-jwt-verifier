import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py_jwt_validator",
    version="0.5.2",
    author="Adrian Lazar",
    author_email="adrian.lazar95@outlook.com",
    description="Python JWT Signature Validator - Asymetric Keys - From exponent and modulus",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adrianlzr/py-jwt-validator",
    keywords="jwt jwt-validator python-jwt-valdidator jwt-signature signature jwt-signature-validator",
    packages=setuptools.find_packages(),
    install_requires=[
        "six",
        "requests",
        "requests_cache"
        ],
    python_requires=">=3",
    project_urls={
        "Documentation & Source":"https://github.com/adrianlzr/py-jwt-validator",
        "Issue Tracker":"https://github.com/adrianlzr/py-jwt-validator/issues"
    },
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Security :: Cryptography "
    ],
)