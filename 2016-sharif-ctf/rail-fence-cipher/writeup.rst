Writeup: SharifCTF 2016 - Rail Fence Cipher
===========================================

:date: 2016-02-07
:tags: security, ctf, sharifctf, crypto
:category: CTF Writeups
:lang: en
:summary: A crypto challenge where you have to get the plain-text from a given
          ciphertext using the *Rail Fence cipher*.


Points
------

**50**


Problem
-------

Decrypt and find the flag:

.. include:: ./data/ciphertext.txt
   :code: text


Theory
------

In the rail fence cipher, the plain-text is written downwards and diagonally
on successive *rails* of an imaginary fence, then moving up when we reach the
bottom rail. When we reach the top rail, the message is written downwards again
until the whole plain-text is written out.
The message is then read off in rows.

For example, if we have ``3`` *rails* and a message of
*WE ARE DISCOVERED. FLEE AT ONCE*, the cipherer writes out:

.. code-block:: text

   W . . . E . . . C . . . R . . . L . . . T . . . E
   . E . R . D . S . O . E . E . F . E . A . O . C .
   . . A . . . I . . . V . . . D . . . E . . . N . .

Then reads off to get the ciphertext:

.. code-block:: text

   WECRL TEERD SOEEF EAOCA IVDEN

*Excerpt from wikipedia*


Solution
--------

The challenge name is *Rail Fence Cipher*, which gave me the insight that
`rail fence` algorithm may be used to generate the ciphertext.

Assuming that cipher algorithm is correct, we need to find the plain-text being
used to generate the ciphertext.

The next step is to try to decode the ciphertext for some rail sizes.

The correct rail size is: ``21`` (with offset: ``0``), which gives the
following plain-text:

.. code-block:: text

   A-fence-is-a-structure-that-encloses-an-area,-SharifCTF{QmFzZTY0IGlzIGEgZ2VuZXJpYyB0ZXJt},-typically-outdoors.

The flag is the string enclosed between ``SharifCTF{`` and ``}``:

.. code-block:: text

   QmFzZTY0IGlzIGEgZ2VuZXJpYyB0ZXJt


Algorithm implementation
------------------------

You can find a Python implementation of the ``Rail Fence cipher`` here:

.. include:: ./src/rail-fence
   :code: python
   :class: highlight

If you want to run the script above, you also need to download the
`shared directory`_ (containing the stuff I share between every CTF) and place
in the same directory of the script.

.. _`shared directory`: https://github.com/alem0lars/ctfs/tree/master/shared
