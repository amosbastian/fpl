from setuptools import setup

setup(
    name="fpl",
    version="0.4.0",
    packages=["fpl"],
    description="A Python wrapper for the Fantasy Premier League API",
    url="https://github.com/amosbastian/fpl",
    author="amosbastian",
    author_email="amosbastian@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python"
    ],
    keywords="fpl fantasy premier league",
    project_urls={
        "Documentation": "http://fpl.readthedocs.io/en/latest/",
        "Source": "https://github.com/amosbastian/fpl"
    },
    install_requires=["requests"]
)
