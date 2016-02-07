Writeup: SharifCTF 2016 - Rail Fence Cipher
===========================================

:date: 2016-02-07
:tags: security, ctf, sharifctf, crypto
:lang: en
:summary: Rail Fence Cipher is a crypto challenge where you have to get
          the plain-text from a given cipher-text using the Rail Fence
          cipher.


Points
------

**50**


Problem
-------

.. code-block::

  Decrypt and find the flag

`Ciphertext`_

.. _`Ciphertext`: ./data/Ciphertext


Solution
--------

We had to decrypt the following cipher-text:

.. code-block::

  AaY--rpyfneJBeaaX0n-,ZZcs-uXeeSVJ-sh2tioaZ}slrg,-ciE-anfGt.-eCIyss-TzprttFliora{GcouhQIadctm0ltt-FYluuezTyorZ-

The challenge name is *Rail Fence Cipher*, which gave me the insight that
`rail fence` algorithm may be used to generate the cipher-text.

Assuming that cipher algorithm is correct, we need to find the plain-text being
used to generate the cipher-text.

The next step is to try to decode the cipher-text for some rail sizes.

The correct rail size is: ``21`` (with offset: ``0``), which gives the
following plain-text:

.. code-block::

  A-fence-is-a-structure-that-encloses-an-area,-SharifCTF{QmFzZTY0IGlzIGEgZ2VuZXJpYyB0ZXJt},-typically-outdoors.

The flag is the string enclosed between ``SharifCTF{`` and ``}``:

.. code-block::

  QmFzZTY0IGlzIGEgZ2VuZXJpYyB0ZXJt


Theory behind
-------------

In the rail fence cipher, the plain-text is written downwards and diagonally
on successive *rails* of an imaginary fence, then moving up when we reach the
bottom rail. When we reach the top rail, the message is written downwards again
until the whole plain-text is written out.
The message is then read off in rows.

For example, if we have ``3`` *rails* and a message of
*WE ARE DISCOVERED. FLEE AT ONCE*, the cipherer writes out:

.. code-block::

  W . . . E . . . C . . . R . . . L . . . T . . . E
  . E . R . D . S . O . E . E . F . E . A . O . C .
  . . A . . . I . . . V . . . D . . . E . . . N . .

Then reads off to get the cipher-text:

.. code-block::

  WECRL TEERD SOEEF EAOCA IVDEN

*Excerpt from wikipedia*


Algorithm implementation
------------------------

You can find a Python implementation of the ``Rail Fence cipher`` here:

.. include:: ./src/rail-fence-cipher
