from setuptools import setup

setup(
    name="fpl",
    version="0.5.1",
    packages=["fpl"],
    description="A Python wrapper for the Fantasy Premier League API",
    url="https://github.com/amosbastian/fpl",
    author="amosbastian",
    author_email="amosbastian@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6"
    ],
    keywords="fpl fantasy premier league",
    project_urls={
        "Documentation": "http://fpl.readthedocs.io/en/latest/",
        "Source": "https://github.com/amosbastian/fpl"
    },
    install_requires=[
        "Click",
        "colorama",
        "PTable",
        "requests",
    ],
    entry_points="""
        [console_scripts]
        fpl=fpl.cli:cli
    """,
)
