<p align="center">
  <a href="https://fpl.readthedocs.io/en/latest/">
    <img src="https://i.imgur.com/ao1t2qN.png">
  </a>
</p>

<p align="center">
    A Python wrapper around the Fantasy Premier League API
    <br>
    <br>
    <a href="https://travis-ci.org/amosbastian/fpl" alt="Build">
        <img src="https://travis-ci.org/amosbastian/fpl.svg?branch=master"/></a>
    <a href="https://fpl.readthedocs.io/en/latest/" alt="Documentation">
        <img src="https://readthedocs.org/projects/fpl/badge/?version=latest" /></a>
    <a href="https://pypi.org/project/fpl/" alt="Version">
        <img src="https://badge.fury.io/py/fpl.svg"/></a>
    <a href="https://pypi.org/project/fpl/" alt="Python version">
        <img src="https://img.shields.io/badge/Python-3.6%2B-blue.svg"/></a>
    <a href="https://www.codacy.com/app/amosbastian/fpl?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=amosbastian/fpl&amp;utm_campaign=Badge_Grade">
        <img src="https://api.codacy.com/project/badge/Grade/8acd6709c8e1402fbcbbc4b7e39bbb98"/></a>
    <a href="https://codecov.io/gh/amosbastian/fpl">
        <img src="https://codecov.io/gh/amosbastian/fpl/branch/master/graph/badge.svg"/></a>
</p>

Join the [Discord server](https://discord.gg/cjY37fv) or submit [an issue](https://github.com/amosbastian/fpl/issues) for help and / or suggestions!

## Installing fpl

The recommended way to install fpl is via `pip`.

    pip install fpl

To install it directly from GitHub you can do the following:

    git clone git://github.com/amosbastian/fpl.git

You can also install a [.tar file](https://github.com/amosbastian/fpl/tarball/master)
or [.zip file](https://github.com/amosbastian/fpl/tarball/master)

    curl -OL https://github.com/amosbastian/fpl/tarball/master
    curl -OL https://github.com/amosbastian/fpl/zipball/master # Windows

Once it has been downloaded you can easily install it using `pip`:

    cd fpl
    pip install .

## Contributing

1. Fork the repository on GitHub.
2. Run the tests with `pytest tests/` to confirm they all pass on your system.
   If the tests fail, then try and find out why this is happening. If you aren't
   able to do this yourself, then don't hesitate to either create an issue on
   GitHub, contact me on Discord or send an email to [amosbastian@gmail.com](mailto:amosbastian@gmail.com>).
3. Either create your feature and then write tests for it, or do this the other
   way around.
4. Run all tests again with with `pytest tests/` to confirm that everything
   still passes, including your newly added test(s).
5. Create a pull request for the main repository's `master` branch.

For more information on how to contribute to **fpl** see [the contributing guide](https://fpl.readthedocs.io/en/latest/contributing/contributing.html).

## Documentation

Documentation and examples for **fpl** can be found at http://fpl.readthedocs.io/en/latest/.
