Writeup: SharifCTF 2016 - uagent
================================

:date: 2016-02-10
:tags: security, ctf, sharifctf, forensics
:category: CTF Writeups
:lang: en
:summary: A challenge where you have to find the flag from a ``.pcap``


Points
------

**100**


Problem
-------

We think we are really cool, are we?

`Download`_

.. _`Download`: {attach}/ctfs/2016-sharif-ctf/uagent/data/ragent.pcap

Solution
--------

First of all, let's try to understand what's going on in the communication, opening
``ragent.pcap`` with *Wireshark*.

It seems to be a HTTP conversation, so let's filter only HTTP packets using the filter:
``http``.

I've noticed there is a strange user agent in all HTTP requests, for example:

.. image:: {attach}/ctfs/2016-sharif-ctf/uagent/data/user-agent-chunk.png
   :alt: A user agent sent in the request.

In that request, the user agent is sctf-app/ChoKAAAADUlIRFIAAAGcAA==/

The ending equals (``==``) let me think the user agent is something encoded in
``base64`` and that particular user agent had two equals as padding.
In fact the length must be multiple of 4; otherwise, there is 1 to 3 equals of padding.

Since in every request the user agent changes, a single user agent may be just a chunk of
the complete data.

Let's try to follow this hypothesis..

I've created a Ruby script (using the external program ``tshark``) that parses ``ragent.pcap``
and builds a data file containing the decoded user agent:

.. include:: ./src/user-agent-extractor.rb
   :code: ruby
   :class: highlight

The output is the following image:

.. image:: {attach}/ctfs/2016-sharif-ctf/uagent/data/user-agent-raw.png
   :alt: Assembled and decoded user agent.

So the image is the password of an archive.. I need to find where the archive is..

Let's take a look at a response:

.. image:: {attach}/ctfs/2016-sharif-ctf/uagent/data/response-chunk-0.png
   :alt: A HTTP response containing the string flag.png.

The response is ``flag.png`` which seems to be the name of the file containing the flag.
Also there is a response header called ``Content-Range`` which contains two numbers.

Taking a look at other responses, some raw bytes are sent:

.. image:: {attach}/ctfs/2016-sharif-ctf/uagent/data/response-chunk-1.png
   :alt: Another HTTP response containing raw bytes.

Maybe the server will send the file ``flag.png`` as response splitted in multiple chunks
and ``Content-Range`` tells the position of the sent bytes inside the final payload.

Let's extract the body response
(*taking care of the response header that controls the chunks ordering*)
with the following script:

.. include:: ./src/resp-body-extractor.rb
   :code: ruby
   :class: highlight

The response is a ``.zip`` archive password-protected. Let's insert the password find above.

The archive only contains the following image (named ``flag.png``):

.. image:: {attach}/ctfs/2016-sharif-ctf/uagent/data/flag.png
   :alt: Flag

The flag is: ``94f7df30fbd061cc4f7294369a8bce1c``.
