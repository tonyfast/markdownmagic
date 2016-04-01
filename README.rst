
markdownmagic
=============

    an `IPython <http://ipython.org/>`__
    `magic <https://ipython.org/ipython-doc/dev/interactive/tutorial.html>`__
    for authoring Interactive Data-Driven notebooks with basic
    `Markdown <>`__.

Install
-------

From the command line (or with ``!`` in a notebook cell):

.. code:: bash

    pip install markdownmagic

Enable
------

Ad-hoc
~~~~~~

In the notebook, you can use the ``%load_ext`` or ``%reload_ext`` line
magic.

.. code:: python

    %reload_ext autoreload
    %autoreload 2

.. code:: python

    from markdownmagic import  environment
    mdmagic = environment()

Configuration
~~~~~~~~~~~~~

In your profile's ``ipython_kernel_config.py``, you can add the
following line to automatically load ``markdownmagic`` into all your
running kernels:

.. code:: python

    c.InteractiveShellApp.extensions = ['markdownmagic']

Use
---

The ``%%jade`` cell magic will either act as simple parser:

.. code:: python

    %%markdown
    # This is markdown
    
    Magic options for markdown:
        
    # How is this different




This is markdown
================

Magic options for markdown:

How is this different
=====================



which can be accessed by the special last result variable ``_``:

.. code:: python

    _




This is markdown
================



Or will update a named variable with the parsed document:

Contribute
----------

`Issues <https://github.com/tonyfast/markdownmagic/issues>`__ and `pull
requests <https://github.com/tonyfast/markdownmagic/pulls>`__ welcome!

License
-------

``markdownmagic`` is released as free software under the `BSD 3-Clause
license <./LICENSE>`__.

Thank
-----

