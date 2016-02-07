Writeup: SharifCTF 2016 - URE
=============================

:date: 2016-02-07
:status: draft
:tags: security, ctf, sharifctf, crypto
:lang: en
:summary: TODO


Points
------

**100**


Problem
-------

Let :math:`p` be a prime, and :math:`g` be an element of :math:`\mathbb{Z}_p^*`
of prime order :math:`q`.

Let :math:`x \in \mathbb{Z}_q` be the private key, and :math:`h = g^x`
(mod :math:`p`) be the public key.

To encrypt a message :math:`m \in \mathbb{Z}_p^*`, pick two random values
:math:`r, s \in \mathbb{Z}_q`, and compute the cipher-text as follows:
:math:`(a, b, c, d) = (g^r, h^r, g^s, mh^s)`.

Download a valid cipher-text :math:`\sigma = (a, b, c, d)` below, and compute
another valid cipher-text :math:`\sigma' = (a', b', c', d')` such that:

1. :math:`\sigma` and :math:`\sigma'` decrypt to the same message;
2. :math:`a \neq a'` and :math:`b \neq b'` and :math:`c \neq c'`
   and :math:`d \neq d'`.

The challenge can be `submitted here`_.

.. _`submitted here`: http://ctf.sharif.edu:34455/chal/URE/eb99c61f69641d9a/
