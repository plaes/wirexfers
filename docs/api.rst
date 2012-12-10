.. _api:

API
===

This part of the documentation covers all the interfaces of WireXfers.

Payment Providers
~~~~~~~~~~~~~~~~~

IPizza
------

.. autoclass:: wirexfers.providers.ipizza.IPizzaProviderBase
   :inherited-members:

IPizza Providers
................

.. autoclass:: wirexfers.providers.ipizza.EEDanskeProvider
   :inherited-members:

.. autoclass:: wirexfers.providers.ipizza.EEKrediidipankProvider
   :inherited-members:

.. autoclass:: wirexfers.providers.ipizza.EELHVProvider
   :inherited-members:

.. autoclass:: wirexfers.providers.ipizza.EESEBProvider
   :inherited-members:

.. autoclass:: wirexfers.providers.ipizza.EESwedBankProvider
   :inherited-members:

Solo/TUPAS
----------

Solo/TUPAS providers
....................

.. autoclass:: wirexfers.providers.tupas.EENordeaProvider
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
