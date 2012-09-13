Flask Quickstart
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
a simple barebones Flask application with required imports:

::

    from flask import Flask, render_template
    app = Flask(__name__)

    @app.route('/')
    def index():
        return 'Hello!'

    if __name__ == '__main__':
        app.run(debug=True)

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

    from flask import Flask, render_template
    from wiretransfers import PaymentInfo, utils
    from wiretransfers.providers import ProviderBase

    app = Flask(__name__)
    # [rest of our flask app]

Now we can load required private and public keys in order to set up
the provider. We also need to supply ``user`` and ``endpoint`` address:

.. code-block:: python
    :emphasize-lines: 5-7

    from flask import Flask, render_template
    from wiretransfers import PaymentInfo, utils
    from wiretransfers.providers import ProviderBase

    private_key = utils.load_key('../_keys_/private_key.pem')
    public_key = utils.load_key('../_keys_/public_key.pem')
    provider = ProviderBase('uuid217657', private_key, public_key, 'https://pangalink.net/banklink/008/ipizza')

    app = Flask(__name__)
    # [rest of our flask app]

Now our provider is configured and can be used to create a payment request.

Making the payment request
--------------------------

In order to make a payment, we first need to create payment information
by filling out relevant fields of :class:`~wiretransfers.PaymentInfo`. Then
we can just call our previously set up ``provider`` to create the payment
request (:class:`~wiretransfers.PaymentRequest`) for us.

Finally we just pass the ``payment_request`` to the template. So let's
modify our ``index`` function a bit:

.. code-block:: python
   :emphasize-lines: 5-7

    # [ rest of our flask app ]

    @app.route('/')
    def index():
        info = PaymentInfo('1.00', 'Test transfer', utils.ref_731('123'))
        payment_request = provider(info)
        return render_template('form.html', payment=payment_request)

    # [ rest of our flask app ]

Now let's create a template under ``templates/form.html``. As we passed
the the ``payment_request`` into template context as ``payment`` variable,
we can now use :attr:`~wiretransfers.PaymentRequest.form`,
:attr:`~wiretransfers.PaymentRequest.payment` and
:attr:`~wiretransfers.PaymentRequest.provider` fields to create a simple
HTML form:

.. code-block:: html+jinja

    <form method="POST" action="{{ payment.provider.endpoint }}">
    {% for item in payment.form -%}
        {% set name, value = item -%}
        <input name="{{ name }}" value="{{ value }}" type="hidden">
    {% endfor -%}
    <dl>
      <dt>Amount:</dt>
      <dd>{{ payment.info.amount }}</dd>
      <dt>Message:</dt>
      <dd>{{ payment.info.message }}</dd>
    </dl>
    <input type="submit">
    </form>

