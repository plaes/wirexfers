Generating private-public keypair
=================================

Generating the private RSA key with 4096-bit keysize::

$ openssl genrsa -out privkey.pem 4096

Generate the Certificate Request::

$ openssl req -new -key privkey.pem -out certificate-request.csr
