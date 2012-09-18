.. _api:

API
===

This part of the documentation covers all the interfaces of WireXfers.

Payment Providers
~~~~~~~~~~~~~~~~~

IPizza
------

Solo/TUPAS
----------

.. autoclass:: wirexfers.providers.tupas.SoloKeyChain
   :inherited-members:

.. autoclass:: wirexfers.providers.tupas.NordeaEEProvider
   :inherited-members:


Base Classes
~~~~~~~~~~~~

.. autoclass:: wirexfers.providers.KeyChainBase
   :inherited-members:

.. autoclass:: wirexfers.providers.ProviderBase
   :inherited-members:

.. automethod:: wirexfers.providers.ProviderBase.__call__

.. autoclass:: wirexfers.PaymentRequest
   :inherited-members:

.. autoclass:: wirexfers.PaymentResponse
   :inherited-members:

Utility Classes
~~~~~~~~~~~~~~~

.. autoclass:: wirexfers.PaymentInfo
   :inherited-members:

Utility Functions
~~~~~~~~~~~~~~~~~

.. automodule:: wirexfers.utils
   :members:
