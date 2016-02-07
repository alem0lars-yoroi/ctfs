Writeup: SharifCTF 2016 - URE
=============================

:date: 2016-02-07
:tags: security, ctf, sharifctf, crypto
:category: CTF Writeups
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
another valid cipher-text
:math:`\sigma^\star = (a^\star, b^\star, c^\star, d^\star)` such that:

1. :math:`\sigma` and :math:`\sigma^\star` decrypt to the same message;
2. :math:`a \neq a^\star` and :math:`b \neq b^\star` and :math:`c \neq c^\star`
   and :math:`d \neq d^\star`.

This is the cipher-text:

.. include:: ./data/ciphertext.txt
   :code: text

To solve the challenge, you need to `submit here`_ the quadruple
:math:`(a^\star, b^\star, c^\star, d^\star)`.
All numbers are assumed to be hexadecimal (without :math:`0x` prefix).

.. _`submit here`:
   http://ctf.sharif.edu:34455/chal/URE/eb99c61f69641d9a/


Theory
------

**Universal Re-encryption** is a *randomized public-key cryptosystem* comprised
by the quadruple of algorithms: :math:`(KG, D, E, Re)`:

- **Key generation algorithm**
  :math:`KG \rightarrow (SK, PK)`:
  It generates both the private key :math:`SK` and the public key :math:`PK`.
- **Decryption algorithm**
  :math:`D(SK, \sigma) \rightarrow m`:
  A deterministic algorithm that takes as input a *secret key* :math:`SK`,
  a *cipher-text* :math:`\sigma` and outputs the *original message* :math:`m`.
- **Encryption algorithm**
  :math:`E(m, f, PK) \rightarrow \sigma`:
  A deterministic algorithm that takes as input a *message* :math:`m`,
  an *encryption factor* :math:`r`, a *public key* :math:`PK` and outputs the
  corresponding cipher-text :math:`\sigma`.
- **Re-encryption algorithm**
  :math:`Re(\sigma, r^\star) \rightarrow \sigma^\star`:
  This algorithm re-randomizes the encryption factor :math:`r^\star`,
  applies it to the provided cipher-text :math:`\sigma`,
  and outputs the new cipher-text :math:`\sigma^\star`.
  The re-encryption is different from the encryption because
  *it is executing without having the knowledge of the message*.
  This makes the re-encryption particularly useful in `mix networks`_
  (technique also used by `Tor`_) where each message is encrypted to each proxy
  (like a `Russian doll`_); but the proxies shouldn't know the message.

The challenge says we shouldn't find the public key.
Furthermore, we already know another cipher-text, but we don't know the message.

*This tells me I need to find and use the re-encryption algorithm.*

Now the question is: there are many ways to implement the quadruple of
algorithms :math:`(KG, D, E, Re)` described above.

*I need to find the which implementation is being used in the challenge..*

.. _`mix networks`: https://en.wikipedia.org/wiki/Mix_network
.. _`Tor`: https://en.wikipedia.org/wiki/Tor_(anonymity_network)
.. _`Russian doll`: https://en.wikipedia.org/wiki/Russian_doll


URE based on ElGamal
~~~~~~~~~~~~~~~~~~~~

- **Initial important note**: if a number :math:`n` belongs to a group
  :math:`\mathbb{Z}_p^*` of prime order :math:`q` (i.e. the group is cyclic);
  then **that number is *mod* :math:`p`**.

Searching on the Internet, I've found the **ElGamal encryption system**.
*The encryption and decryption functions seem to be really similar to the ones
described in the challenge*. But that algorithm by default doesn't implement
the 4th algorithm, i.e. the *re-encryption* algorithm which is the algorithm
I need to use to get another cipher-text corresponding to the same original
message.

The *URE* algorithms implementation based on *ElGamal* is
(source `Philippe Golle`_):

- **Key generation**: :math:`KG \rightarrow (SK = x, PK = g^x)`.
  The public key is computed as :math:`PK = g^x` using the generated private
  key :math:`x` and a generator called
  :math:`g \in \mathbb{Z}_p^*` of prime order :math:`q` (i.e. cyclic group).

- **Decryption algorithm**: If :math:`b / a = 1`, then
  :math:`D(SK, \sigma = (a, b, c, d)) \rightarrow m = d / c^{SK}`;
  otherwise, the decryption is failed.
  Notice that :math:`a, b, c, d \in \mathbb{Z}_p^*`
  (their value is *mod* :math:`p`).

- **Encryption algorithm**:

  .. math::

     E(m, r = (r_0, r_1), PK)
     \rightarrow
     \sigma = (a = g^{r_0}, b = PK^{r_0}, c = g^{r_1}, d= m \cdot PK^{r_1})

  Notice that the computed :math:`a, b, c, d \in \mathbb{Z}_p^*`
  (their value is *mod* :math:`p`).

- **Re-encryption algorithm**:

  .. math::

     Re(\sigma = (a, b, c, d), r^\star = (r_0^\star, r_1^\star))
     \rightarrow
     \sigma^\star = (a^\star = a^{r_0^\star},
                     b^\star = b^{r_0^\star},
                     c^\star = c \cdot a^{r_1^\star},
                     d^\star = d \cdot b^{r_1^\star})

  Notice that the computed
  :math:`a^\star, b^\star, c^\star, d^\star \in \mathbb{Z}_p^*`
  (their value is *mod* :math:`p`).

.. _`Philippe Golle`: http://crypto.stanford.edu/~pgolle


Solution
--------

I need to choose a valid value of :math:`r^\star = (r_0^\star, r_1^\star)`
in order to generate a cipher-text
:math:`\sigma^\star = (a^\star, b^\star, c^\star, d^\star)`
compliant with the constraint:
:math:`a \neq a^\star, b \neq b^\star, c \neq c^\star, d \neq d^\star`.

I need to choose :math:`r_0^\star \neq 1`, otherwise I get
:math:`a = a^\star, b = b^\star`, which isn't complaint with the constraint.

Trying with :math:`r_0^\star = 2, r_1^\star = 1`, I get:

.. math::

   \sigma^\star = (a^\star = a \cdot a,
                   b^\star = b \cdot b,
                   c^\star = c \cdot a,
                   d^\star = d \cdot b)

I have to remember that
:math:`a^\star, b^\star, c^\star, d^\star \in \mathbb{Z}_p^*`
(their value is *mod* :math:`p`), so *the final formula is*:

.. math::

   \sigma^\star = (a^\star = (a \cdot a) \text{ mod } p,
                   b^\star = (b \cdot b) \text{ mod } p,
                   c^\star = (c \cdot a) \text{ mod } p,
                   d^\star = (d \cdot b) \text{ mod } p)

Replacing the input cipher-text :math:`\sigma` with its value,
I get the following generated cipher-text :math:`\sigma^\star`:

.. math::

   a^\star = 328740669304003745433811770374618618513213791478583575295060

             484577741575836061536078443289812818578289443615404803640652

             3549199332371675403330587908658389

   b^\star = 310636155853689619831549062791702025703998507804509192532516

             793075601277521902177827453831628795715318450107651338982252

             9518252243096913454042609623430979

   c^\star = 270574947117841158171075930391740671179784850991752897501849

             703687602486209121458065933993292991263374384128127520038126

             1759865873903109533343463983599973

   d^\star = 537348303914229578514680504904642332655557132609224534787109

             113866484311290252304047334217101763950152496116172075869334

             3930112103298610080325764680063048


Algorithm implementation
------------------------

You can find a Python implementation of the ``URE based on ElGamal`` here:

.. include:: ./src/ure
   :code: python
   :class: highlight
