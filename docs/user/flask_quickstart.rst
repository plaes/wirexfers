Flask quickstart
================

This section should give you an introduction of integrating WireTransfers
into a `Flask <http://flask.pocoo.org>`_ application and therefore it
assumes that you have Flask installed.

It also expects that you already have the required credentials from one
of the supported banks. Test credentials can also be obtained from
`pangalink.net <http://pangalink.net>`_.

Minimal application
-------------------

It's probably easiest to start from the beginning, so we start by making
a simple barebones Flask application:

::

    from flask import Flask
    app = Flask(__name__)

    @app.route('/')
    def index():
        return 'Hello!'

    if __name__ == '__main__':
        app.run()

Just save it as ``testapp.py``. Just make sure it's not called ``flask.py``
or ``wiretransfers.py`` because it would break everything. Now try executing
it with your Python interpreter (please note that output on your machine
might be a bit different):

::

    $ python testapp.py
     * Running on http://127.0.0.1:5000/

Setting up the provider
-----------------------

First, we have to make sure that required interfaces are available in our
Flask application. Therefore we need to import
:class:`wiretransfers.providers.ProviderBase` and
:class:`wiretransfers.PaymentInfo`. It's also nice to have
:mod:`wiretransfers.utils` available.

.. code-block:: python
    :emphasize-lines: 2,3

    from flask import Flask
    from wiretransfers import PaymentInfo, utils
    from wiretransfers.providers import ProviderBase

    app = Flask(__name__)
    # [rest of our flask app]

Now we can load required private and public keys in order to set up
the provider. We also need to supply ``user`` and ``endpoint`` address:

.. code-block:: python
    :emphasize-lines: 5-7

    from flask import Flask
    from wiretransfers import PaymentInfo, utils
    from wiretransfers.providers import ProviderBase

    private_key = utils.load_key('../_keys_/private_key.pem')
    public_key = utils.load_key('../_keys_/public_key.pem')
    provider = ProviderBase('uuid217657', private_key, public_key, 'https://pangalink.net/banklink/008/ipizza')

    app = Flask(__name__)
    # [rest of our flask app]

Now our provider is configured and can be used to make payments. And our
application code should be following:

.. code-block:: python

    from flask import Flask
    from wiretransfers import PaymentInfo, utils
    from wiretransfers.providers import ProviderBase

    private_key = utils.load_key('../_keys_/private_key.pem')
    public_key = utils.load_key('../_keys_/public_key.pem')
    provider = ProviderBase('uuid217657', private_key, public_key, 'https://pangalink.net/banklink/008/ipizza')

    app = Flask(__name__)

    @app.route('/')
    def index():
        return 'Hello!'

    if __name__ == '__main__':
        app.run()
