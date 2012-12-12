Using WireXfers
===============

This section should give you an introduction on how to integreate WireXfers
with various applications and web frameworks.

.. note::

    Code snippets below use pseudocode and will not work when using them in
    real application. Consult framework-specific examples for real working
    code.

Basic flow of the payment process is following:

#. Initialize provider-specific keychain
#. Initialize provider
#. Create payment information
#. Show user the payment form which takes him to provider page
#. Process the return results

Setting up the provider
-----------------------

Each provider has to be initialized by provider-specific keychain. Depending on
keychain, its arguments are either simple strings (Solo/TUPAS) or consists of
private/public key pair objects (IPizza).

.. code-block:: python

    from wirexfers.providers import PseudoProvider

    # Create and initialize provider-specific keychain
    keychain = PseudoProvider.KeyChain(...)

    # Create and initialize the provider
    #: user - user id used at provider's side
    #: endpoint - endpoint address where to send payment request
    provider = PseudoProvider(user, keychain, endpoint)

Creating the payment and initializing the payment request
---------------------------------------------------------

In order to make a payment, we first need to set up a payment information
by filling out relevant fields of :class:`~wirexfers.PaymentInfo`.

.. code-block:: python

    from wirexfers import PaymentInfo, utils
    info = PaymentInfo('1.00', 'Test transfer', utils.ref_731('123'))


Now that we have the `PaymentInfo`, in order to create a payment request, we
have to create a dictionary containing return urls to views where our application
handles the payment response.

.. note::

    Return url support varies with providers. Please consult each providers
    documentation to see which return urls are supported. By default we need
    at least the ``return`` URL.

.. note::

   Return urls should be absolute!
    
.. code-block:: python

    urls = {'return': 'http://example.com'}

With that, everything we need to create a payment request
(:class:`~wirexfers.PaymentRequest`) has been done:

.. code-block:: python

   payment = provider(info, urls)

All we need now is to pass the ``payment`` info into template and create
a HTML form visible to the user:


This is all from application side, we just have to pass the ``payment`` to the
template in order to show the payment form to the user. Lets assume that
payment request has been passed into template context as ``payment`` variable,
so can use :attr:`~wirexfers.PaymentRequest.form` iterator to create form
fields, :attr:`~wirexfers.PaymentRequest.info` to display the payment
information and various :attr:`~wirexfers.PaymentRequest.provider` fields to
initialize a simple HTML form.

Basic Jinja2 template should look like this:

.. code-block:: html+jinja

    <form method="POST" action="{{ payment.provider.endpoint }}" accept-charset="{{ payment.provider.form_charset }}">
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

.. note::

    Depending on the provider, we need either handle single or multiple return
    urls.

.. note::

    Depending on the provider we need to either handle GET or POST request data.

.. note::

    Depending on the provider we also need to handle responses in non-utf8
    charsets.

In order to verify payment status, we just need to parse the request
data using :meth:`~wirexfers.providers.ProviderBase.parse_response`.
This create a :class:`~wirexfers.PaymentResponse` which contains
:attr:`~wirexfers.PaymentResponse.is_valid` and various other data related to
payment.

.. code-block:: python

    from wirexfers.exc import InvalidResponseError
    # data contains either POST or GET request data
    try:
        payment = provider.parser_response(data)
    except InvalidResponseError
        # Signature failure, we should redirect to proper error page
        pass

    if payment.is_valid:
        # Show "Successful order page!"
    else:
        # Show "Order failure page"

And that's basically how it works! :)
