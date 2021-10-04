Installation
============

From Pypi
---------

The easiest way is to install via pypi via:

``pip install checkcert``

If you already have checkcert installed and wish to update it, run:

``pip install -U checkcert``

This will upgrade the currently-installed version to the latest.

From Git
--------

There are many methods for running within a virtual environment isolated for a particular package.  Certcheck has been built with poetry, so this document details that method, but there are certainly other ways to accomplish the same thing

1. clone the repo ``git clone https://github.com/kellya/checkcert.git``
2. cd to the directory you just cloned ``cd checkcert``
3. install the required packages ``poetry install``
4. activate the poetry-built venv ``poetry shell``
5. run with ``python certcheck/certcheck.py``
