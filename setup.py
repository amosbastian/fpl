from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="fpl",
    version="0.6.19",
    packages=find_packages(),
    description="A Python wrapper for the Fantasy Premier League API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amosbastian/fpl",
    author="amosbastian",
    author_email="amosbastian@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7"
    ],
    keywords="fpl fantasy premier league",
    project_urls={
        "Documentation": "http://fpl.readthedocs.io/en/latest/",
        "Source": "https://github.com/amosbastian/fpl"
    },
    install_requires=[
        "Click",
        "colorama",
        "codecov",
        "PTable",
        "appdirs",
        "aiohttp",
        "pytest-aiohttp",
        "pytest-cov",
        "pytest-mock",
        "pytest",
        "requests"
    ],
    entry_points="""
        [console_scripts]
        fpl=fpl.cli:cli
    """,
)
