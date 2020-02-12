import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py_jwt_verifier",
    version="0.7.0",
    author="Adrian Lazar",
    author_email="adrian.lazar95@outlook.com",
    description="Python JWT Verfier - Verifies the signature of a digitally signed JWT.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adrianlzr/py-jwt-verifier",
    keywords="python jwt verifier, jwt verifier, jwt signature verifier, py-jwt-verifier, python-jwt-verifier, python jwt signature verifier",
    packages=setuptools.find_packages(),
    install_requires=[
        "six",
        "requests",
        "requests_cache"
        ],
    python_requires=">=3",
    project_urls={
        "Documentation & Source":"https://github.com/adrianlzr/py-jwt-verifier",
        "Issue Tracker":"https://github.com/adrianlzr/py-jwt-verifier/issues"
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