.. _api:

API
===

This part of the documentation covers all the interfaces of WireXfers.

Payment Providers
~~~~~~~~~~~~~~~~~

IPizza
------

.. autoclass:: wirexfers.providers.ipizza.IPizzaKeyChain
   :inherited-members:

.. autoclass:: wirexfers.providers.ipizza.IPizzaProviderBase
   :inherited-members:

IPizza Providers
................

Solo/TUPAS
----------

.. autoclass:: wirexfers.providers.tupas.SoloKeyChain
   :inherited-members:

Solo/TUPAS providers
....................

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

Exceptions
~~~~~~~~~~

.. automodule:: wirexfers.exc
   :show-inheritance:
   :members:

Utility Classes
~~~~~~~~~~~~~~~

.. autoclass:: wirexfers.PaymentInfo
   :inherited-members:

Utility Functions
~~~~~~~~~~~~~~~~~

.. automodule:: wirexfers.utils
   :members:
