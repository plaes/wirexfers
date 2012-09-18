Flask Quickstart
================

This section should give you an introduction of integrating WireXfers
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
        app.run(debug=True)

Just save it as ``testapp.py``. Just make sure it's not called ``flask.py``
or ``wirexfers.py`` because it would break everything. Now try executing
it with your Python interpreter (please note that output on your machine
might be a bit different):

::

    $ python testapp.py
     * Running on http://127.0.0.1:5000/

Setting up the provider
-----------------------

.. warning::

    In this tutorial we are going to use Nordea Estonia's Solo/TUPAS as an
    example, mainly because they have official test system available. You still
    need to figure out a way to acquire credentials for it and this is left as
    an exercise to the reader. Sorry! ;)

In order to set up a provider, we first need to create a keychain. As payment
providers use different credential system (private/public key, simple password)
the keychain is used to hide away the low-level details of credential handling.

:class:`wirexfers.providers.tupas.NordeaEEProvider` uses
:class:`wirexfers.providers.tupas.SoloKeyChain` requiring a single
bank-provided *MAC-key*:

.. code-block:: python

    from wirexfers.providers.tupas import SoloKeyChain
    # Replace the '<mac>' argument below!
    keychain = SoloKeyChain(<mac>)

.. note::

    Previous keychain setup is specific to
    :class:`~wirexfers.providers.tupas.NordeaEEProvider`. Other providers may
    require different KeyChain setup. Please consult the documentation of each
    provider.


Now that we have created our keychain, setting up the provider is a breeze:

.. code-block:: python

    from wirexfers.providers.tupas import NordeaEEProvider
    # Replace the <user> and <endpoint> arguments below!
    provider = NordeaEEProvider(<user>, keychain, <endpoint>)

And that's all - now our provider is configured and can be used to initiate
payment request. Our current application so far looks like this:

.. code-block:: python
   :emphasize-lines: 2, 5-9

    from flask import Flask
    from wirexfers.providers.tupas import SoloKeyChain, NordeaEEProvider

    app = Flask(__name__)

    # Replace the '<mac>' argument below!
    keychain = SoloKeyChain(<mac>)
    # Replace the <user> and <endpoint> arguments below!
    provider = NordeaEEProvider(<user>, keychain, <endpoint>)

    @app.route('/')
    def index():
        return 'Hello!'

    if __name__ == '__main__':
        app.run(debug=True)


Making the payment request
--------------------------

In order to make a payment, we first need to set up a payment information
by filling out relevant fields of :class:`~wirexfers.PaymentInfo`. Because the
payment are usually made within a request, we need to plug it into our view
function:

.. code-block:: python

    from wirexfers import PaymentInfo, utils
    info = PaymentInfo('1.00', 'Test transfer', utils.ref_731('123'))

Next we need to decide our return urls. Though we currently don't yet handle
the urls, but they still needed so provider knows where to direct user after
payment operation.

.. note::

    Return url support varies with providers. Please consult each providers
    documentation to see which return urls are supported.

:class:`~wirexfers.providers.tupas.NordeaEEProvider` requires following return
urls:

 * ``cancel`` - user cancels the payment
 * ``reject`` - bank rejects the payment (not enough funds, ...)
 * ``return`` - successful payment

Although we don't yet handle these URLs, we still need to fill them out because
payment provider expects them along with payment request.  Therefore we just
simply point these urls to the ``/index`` view and utilize Flask's
:meth:`~Flask.url_for()` along with ``_external=True`` argument to make the
URLs absolute:

.. code-block:: python

    urls = {'cancel': url_for('index', _external=True),
            'reject': url_for('index', _external=True),
            'return': url_for('index', _external=True)}

Now everything has been set up, so we just call our previously initialized
``provider`` with ``payment`` and ``urls`` arguments in order to create the
payment request (:class:`~wirexfers.PaymentRequest`) for us:

.. code-block:: python

   payment = provider(info, urls)

This is all from application side, we just have to pass the ``payment`` to the
template in order to show the payment form to the user:

.. code-block:: python
   :emphasize-lines: 14-19

    from flask import Flask, render_template, url_for
    from wirexfers import PaymentInfo, utils
    from wirexfers.providers.tupas import SoloKeyChain, NordeaEEProvider

    app = Flask(__name__)

    # Replace the '<mac>' argument below!
    keychain = SoloKeyChain(<mac>)
    # Replace the <user> and <endpoint> arguments below!
    provider = NordeaEEProvider(<user>, keychain, <endpoint>)

    @app.route('/')
    def index():
        info = PaymentInfo('1.00', 'Test transfer', utils.ref_731('123'))
        urls = {'cancel': url_for('index', _external=True),
                'reject': url_for('index', _external=True),
                'return': url_for('index', _external=True)}
        payment = provider(info, urls)
        return render_template('form.html', payment=payment)

    if __name__ == '__main__':
        app.run(debug=True)

We are still missing the template, though! Open up the As we are passing the
payment request into template context as ``payment`` variable, we can now use
:attr:`~wirexfers.PaymentRequest.form`, :attr:`~wirexfers.PaymentRequest.info`
and :attr:`~wirexfers.PaymentRequest.provider` fields to create a simple HTML
form.  So open up ``templates/form.html`` and make sure it contains this:

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


Handling the Payment response
-----------------------------

.. warning::

   This section is using :class:`~wirexfers.providers.tupas.NordeaEEProvider`
   as an example. Consult documentation on how to handle specific provider.

Let's start by adding new views to handle payment different request responses
and modify our ``urls`` dictionary to use those views:

.. code-block:: python
    :emphasize-lines: 1-3

    urls = {'cancel': url_for('cancel', _external=True),
            'reject': url_for('reject', _external=True),
            'return': url_for('finish', _external=True)}

    @app.route('/cancel')
    def cancel():
        return 'Payment cancelled!'

    @app.route('/reject')
    def reject():
        return 'Payment rejected!'

    @app.route('/finish')
    def finish():
        return 'Payment successful!'

.. note::

   :class:`~wirexfers.providers.tupas.NordeaEEProvider` uses ``GET`` request
   method to handle payment responses. This may be different for other
   providers.

We also create view for invalid response:

.. code-block:: python

    @app.route('/invalid')
    def invalid():
        return 'INVALID PAYMENT'

As :class:`~wirexfers.providers.tupas.NordeaEEProvider` uses ``GET`` request
for payment status confirmation, therefore we just need to parse that in every
view and check whether it's valid:

.. code-block:: python

    from flask import redirect, request
    payment = provider.parse_response(request.args)
    if payment.is_valid:
        # Do something with the result
        return payment.data
    return redirect(url_for('invalid'))
