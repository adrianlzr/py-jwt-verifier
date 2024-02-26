import platform
import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

urllib3_version = "<2.0"
major, minor, patchlevel = platform.python_version_tuple()
if int(major) == 3 and int(minor) > 7:
    urllib3_version = ">=2.0"

setuptools.setup(
    name="py_jwt_verifier",
    version="0.8.0",
    author="Adrian Lazar",
    author_email="adrian.lazar95@outlook.com",
    description="Python JWT Verfier - Verifies the signature of a digitally signed JWT.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adrianlzr/py-jwt-verifier",
    keywords="python jwt verifier, jwt verifier, jwt signature verifier, py-jwt-verifier, python-jwt-verifier, python jwt signature verifier",
    packages=setuptools.find_packages(),
    install_requires=[
        "requests >=2.31.0, <2.40.0",
        "requests_cache >=1.2.0, <1.3.0",
        "urllib3%s" % urllib3_version,
    ],
    python_requires=">=3.8.0",
    project_urls={
        "Documentation & Source": "https://github.com/adrianlzr/py-jwt-verifier",
        "Issue Tracker": "https://github.com/adrianlzr/py-jwt-verifier/issues",
    },
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Security :: Cryptography ",
    ],
)
