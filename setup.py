from glob import glob
from os.path import basename, splitext

from setuptools import find_packages, setup

VERSION = "1.0.2"
README_PATH = "docs/README.md"

# test_requirements = ["behave", "behave-classy", "pytest"]

long_description = ""
with open(README_PATH, "r", encoding="utf-8") as file:
    long_description = file.read()

setup(
    name="yconverter",
    version=VERSION,
    license="Apache Software License 2.0",
    description="All fiat currency and crypto converter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Yunus Emre Ak",
    author_email="yemreak.com@gmail.com",
    url="https://github.com/yedhrab/YConverter",
    packages=find_packages(),
    py_modules=[splitext(basename(path))[0] for path in glob("*.py")],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Utilities",
    ],
    project_urls={
        "Changelog": "https://github.com/yedhrab/YConverter/blob/main/CHANGELOG.md",
        "Issue Tracker": "https://github.com/yedhrab/YConverter/issues",
    },
    keywords=[
        "cryptocurrencyconverter",
        "currencyconverter",
        "converter",
        "currecies",
        "crpytocurrencies",
        "cryptoconverter",
    ],
    python_requires=">=3.10",
    install_requires=["ruamel.yaml==0.17.21", "requests==2.27.1"],
    entry_points={"console_scripts": ["convert = yconverter.cli:main"]},
)
