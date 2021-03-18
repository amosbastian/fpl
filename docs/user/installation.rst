.. _installation:

Installing **fpl**
==================

The recommended way to install ``fpl`` is via ``pip``.

.. code-block:: bash

   pip install fpl

.. note:: Depending on your system, you may need to use ``pip3`` to install
          packages for Python 3.

Updating **fpl** with pip
-------------------------

To update **fpl** you can run:

.. code-block:: bash

   pip install --upgrade fpl

Example output:

.. code-block:: bash

    Installing collected packages: fpl
      Found existing installation: fpl 0.1.0
        Uninstalling fpl-0.1.0:
          Successfully uninstalled fpl-0.1.0
    Successfully installed fpl-0.2.0

Installing older versions
-------------------------

Older versions of **fpl** can be installed by specifying the version number
as part of the installation command:

.. code-block:: bash

   pip install fpl==0.2.0

Installing from GitHub
----------------------

The source code for **fpl** is available on GitHub repository
`<https://github.com/amosbastian/fpl>`_. To install the most recent
version of **fpl** from here you can use the following command::

    $ git clone git://github.com/amosbastian/fpl.git

You can also install a `.tar file <https://github.com/amosbastian/fpl/tarball/master>`_
or `.zip file <https://github.com/amosbastian/fpl/tarball/master>`_

    $ curl -OL https://github.com/amosbastian/fpl/tarball/master
    $ curl -OL https://github.com/amosbastian/fpl/zipball/master # Windows

Once it has been downloaded you can easily install it using `pip`::

    $ cd fpl
    $ pip install .
