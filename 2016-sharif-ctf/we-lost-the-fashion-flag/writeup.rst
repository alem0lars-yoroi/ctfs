Writeup: SharifCTF 2016 - We lost the fashion flag
==================================================

:date: 2016-02-10
:tags: security, ctf, sharifctf, forensics
:category: CTF Writeups
:lang: en
:summary: A challenge where I have to find the flag stored with an unknown
          compression method.


Points
------

**100**


Problem
-------

In Sharif CTF we have lots of task ready to use, so we stored their data about
author or creation date and other related information in some files.
But one of our staff used a method to store data efficiently and left the
group some days ago.
So if you want the flag for this task, you have to find it yourself!


`Download`_

.. _`Download`:
   {attach}/ctfs/2016-sharif-ctf/we-lost-the-fashion-flag/data/fashion.tar.gz

Solution
--------

First of all, let's extract the archive:

.. code-block:: shell-session

   $ tar xzf fashion.tar.gz
   $ tar xzf sharif_tasks.tgz

We get the following files:

- ``fashion.model`` data file.
- ``out`` directory, containing a lot of data files.

Let's examine ``fashion.model``..

These are the some ascii strings contained:

.. code-block:: text

   FemtoZip
   4}', 'ctf': 'Shairf CTF', 'points': 265,4}', 'ctf': 'Shairf CTF', 'points': 280, 'year': 2014}', 'ctf': 'Shairf CTF', 'points': 325, 'year': 2015}', 'ctf': 'Shairf CTF', 'points': 235, 'year': 2015}', 'ctf': 'Shairf CTF', 'points': 255, 'year': 2016}', 'ctf': 'Shairf CTF', 'points': 100, 'year': 2016}', 'ctf': 'Shairf CTF', 'points': 160, 'year': 2016}', 'ctf': 'Shairf CTF', 'points': 285, 'year': 2016}', 'ctf': 'Shairf CTF', 'points': 295, 'year': 2017}', 'ctf': 'Shairf CTF', 'points': 115, 'year': 2017}', 'ctf': 'Shairf CTF', 'points': 200, 'year': 2017}', 'ctf': 'Shairf CTF', 'points': 265, 'year': 2017}', 'ctf': 'Shairf CTF', 'points': 300, 'year': 2018}', 'ctf': 'Shairf CTF', 'points': 160, 'year': 2018}', 'ctf': 'Shairf CTF', 'points': 170, 'year': 2018}', 'ctf': 'Shairf CTF', 'points': 180, 'year': 2018}', 'ctf': 'Shairf CTF', 'points': 195, 'year': 2018}', 'ctf': 'Shairf CTF', 'points': 215, 'year': 2018}', 'ctf': 'Shairf CTF', 'points': 275, 'year': 2018}', 'ctf': 'Shairf CTF', 'points':
   ...

It seems that ``FemtoZip`` is the magic-number.

The rest is some sort of JSON-like data. It seems to be the description (i.e. model) of the ``out`` data files.

Looking on the Internet for ``FemtoZip`` I've found it's a `compression algorithm`_.

Let's try to compile it:

.. code-block:: shell-session

   $ git clone https://github.com/gtoubassi/femtozip.git
   $ cd femptozip/cpp
   $ ./configure
   $ make
   $ cd ./fzip/src

The executable ``fzip`` has been generated.

This is its usage:

.. code-block:: shell-session

   $ ./fzip --help

     Must specify one of --compress, --decompress, or --build

     basic usage: --model <path> --build|compress|decompress  <path> ...
            <path>       All files to be operated on (compressed/decompressed or
                         used for model building).  If path is a directory, then
                         all files within path are inputs
            --model      The path where the model should be saved (if --build) or
                         loaded (if --compress or --decompress)
            --build      Build a new model or sdch dictionary (saved to model path)
            --compress   Compress all files specified or files contained in
                         specified directory
            --decompress Decompress all files specified or files contained in
                         specified directory
            --dictonly   If specified with --build, only write the dictionary to the
                         model path.  useful for SDCH dictionary building
            --verbose    Output status updates and timings
            --benchmark  Output timings and don't actually write compressed or
                         decompressed files (non destructive so can be rerun)
            --maxdict    If specified with --build, limit the dictionary to the
                         specified number of bytes (default and max are 64k)
            --level      Speed vs compression ratio.  0 means fast, 9 means highly
                         compressed

- The file ``fashion.model`` is the value we should pass to the argument ``--model``.
- The operation needed is ``--decompress`` (because ``out`` directory contains the compressed data).

.. code-block:: shell-session

   $ ./fzip --model /path/to/fashion.model --decompress /path/to/out

Now the single files included in the directory ``out`` are decompressed.

Taking a look at some of those, they contain the informations about SharifCTFs challenges,
like: challenge name, points given, year, *flag*.

I need to find the data relative to the challenge *We lost the fashion flag*
(giving *100 points*) of *SharifCTF* in *2016*:

.. code-block:: shell-session

   $ grep -E "'category': 'forensic'.*Fashion.*'points': 100.*'year': 2016" /path/to/out/*

   11180:{'category': 'forensic', 'author': 'staff_3', 'challenge': 'Fashion', 'flag': 'SharifCTF{2b9cb0a67a536ff9f455de0bd729cf57}', 'ctf': 'Shairf CTF', 'points': 100, 'year': 2016}
   11223:{'category': 'forensic', 'author': 'staff_5', 'challenge': 'Fashion', 'flag': 'SharifCTF{41160e78ad2413765021729165991b54}', 'ctf': 'Shairf CTF', 'points': 100, 'year': 2016}
   11908:{'category': 'forensic', 'author': 'staff_2', 'challenge': 'Fashion', 'flag': 'SharifCTF{8725330d5ffde9a7f452662365a042be}', 'ctf': 'Shairf CTF', 'points': 100, 'year': 2016}
   273:{'category': 'forensic', 'author': 'staff_3', 'challenge': 'Fashion', 'flag': 'SharifCTF{1bc898076c940784eb329d9cd1082a6d}', 'ctf': 'Shairf CTF', 'points': 100, 'year': 2016}
   9401:{'category': 'forensic', 'author': 'staff_6', 'challenge': 'Fashion', 'flag': 'SharifCTF{c19285fd5d56c13b169857d863a1b437}', 'ctf': 'Shairf CTF', 'points': 100, 'year': 2016}

The flag is: ``2b9cb0a67a536ff9f455de0bd729cf57``.

.. _`compression algorithm`: https://github.com/gtoubassi/femtozip
