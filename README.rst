WireXfers [waɪə trænsfɜːz]
==========================

WireXfers is an online payments library, written in Python, supporting
various online payment protocols (IPizza, Solo/TUPAS) using a simple API.

Features
--------

- Single API for different providers
- Supported protocols:

  * IPizza

    * LHV Bank (Estonia)
    * SEB Bank (Estonia)
    * SwedBank (Estonia)

  * Solo/TUPAS

    * Nordea Bank (Estonia)

Installation
------------

To install WireXfers, simply: ::

    $ pip install wirexfers

Or, if you absolutely must: ::

    $ easy_install wirexfers

But, you really shouldn't do that.

Usage example
-------------

Basic usage in pseudocode: ::

    # Set up provider-specific keychain
    keychain = KeyChain(...)

    # Configuring the provider
    provider = PaymentProtocol(user, keychain, endpoint)

    # Creating the payment request
    payment = provider(payment_info, return_urls)

    # Parsing the payment response
    response = provider.parse_response(request.form)
    if response.successful:
        # do something
    else:
        # report failure
