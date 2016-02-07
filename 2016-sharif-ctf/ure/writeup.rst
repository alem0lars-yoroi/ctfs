Writeup: SharifCTF 2016 - URE
=============================

:status: draft
:tags: security, ctf, sharifctf, crypto
:lang: en
:summary: TODO


Points
------

**100**


Problem
-------

Let :math:`p` be a prime, and :math:`g` be an element of :math:`ℤ_p^*` of
prime order q.

Let :mathx ∈ ℤq be the private key, and h = gx (mod p) be the public key.

To encrypt a message m ∈ ℤ
*
p
  , pick two random values r, s ∈ ℤq, and compute the ciphertext as follows:
(a, b, c, d) = (gr, hr, gs, mhs).

Download a valid ciphertext σ = (a, b, c, d) below, and compute another valid ciphertext σ′ = (a′, b′, c′, d′) such that:

    σ and σ′ decrypt to the same message;
    a ≠ a′ and b ≠ b′ and c ≠ c′ and d ≠ d′. 


http://ctf.sharif.edu:34455/chal/URE/eb99c61f69641d9a/
