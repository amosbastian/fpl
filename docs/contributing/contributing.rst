.. _contributing:

Contributing
============

If you're reading this, then you're probably interested in helping out with
the development of `fpl`! On this page you will be able to find information
that *should* make it easier for you to start contributing. Since contributions
can be in all kinds of different forms, the contributing guide has been split
up into sections.

To contact me directly you can add me on Discord (Amos#4622) or send an email
to `amosbastian@gmail.com <mailto:amosbastian@gmail.com>`_.

Code contributions
------------------

Submitting code
~~~~~~~~~~~~~~~

When contributing code, you'll want to follow this checklist:

1. Fork the repository on GitHub.
2. Run the tests with `pytest tests/` to confirm they all pass on your system.
   If the tests fail, then try and find out why this is happening. If you aren't
   able to do this yourself, then don't hesitate to either create an issue on
   GitHub (see :ref:`reporting-bugs`), contact me on Discord or send an email
   to `amosbastian@gmail.com <mailto:amosbastian@gmail.com>`_.
3. Either create your feature and then write tests for it, or do this the other
   way around.
4. Run all tests again with with `pytest tests/` to confirm that everything
   still passes, including your newly added test(s).
5. Create a pull request for the main repository's ``master`` branch.

If you want, you can also add your name `AUTHORS <https://github.com/amosbastian/fpl/blob/master/AUTHORS.rst>`_.

Code review
~~~~~~~~~~~

Currently I am the only maintainer of this project. Because of this I will review
each pull request myself and provide feedback if necessary. I would like this to
happen in a clear and calm manner (from both sides)!

New contributors
~~~~~~~~~~~~~~~~

If you are new or relatively new to contributing to open source projects, then
please don't hesitate to contact me directly! I am more than willing to help
out, and will try and assign issues to you if possible.

Code style
~~~~~~~~~~

The `fpl` package follows `PEP 8`_ code style. Currently there is only one
specific additions to this, but if you think more should be added, then this
can always be discussed.

- Always use double-quoted strings, unless it is not possible.

.. _PEP 8: https://pep8.org/

Documentation contributions
---------------------------

Documentation improvements and suggestions are always welcome! The
documentation files live in the ``docs/`` directory. They're written in
`reStructuredText`_, and use `Sphinx`_ to generate the full suite of
documentation.

Of course the documentation doesn't have to be too serious, but try and keep it
semi-formal.

.. _reStructuredText: http://docutils.sourceforge.net/rst.html
.. _Sphinx: http://sphinx-doc.org/index.html


.. _reporting-bugs:

Reporting bugs
--------------

If you encounter any bugs while using **fpl** then please don't hesitate to
open an issue. However, before you do, please check the `GitHub issues`_ (make
sure to also check closed ones) to see if the bug has already been reported.

A template is provided below to make it easier to understand the issue:

.. code-block:: none

    #### Expected behaviour
    What did you expect to happen?

    #### Actual behaviour
    What actually happened?

    #### How to reproduce
    When did it happen? Include a code snippet if possible!

.. _GitHub issues: https://github.com/amosbastian/fpl/issues


Feature requests
----------------

Currently **fpl** is in active development, so feature requests are more than
welcome. If you have any ideas for features you'd like to see added, then
simply create an `issue`_ with an **enhancement** label.

.. _issue: https://github.com/amosbastian/fpl/issues
