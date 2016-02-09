Writeup: SharifCTF 2016 - dMd
===========================================

:date: 2016-02-07
:tags: security, ctf, sharifctf, reverse
:category: CTF Writeups
:lang: en
:summary: A reverse challenge where I should find the expected password.


Points
------

**50**


Problem
-------

Flag is : The valid input

`Download the binary`_

.. _`Download the binary`: {attach}/ctfs/2016-sharif-ctf/dmd/data/dMd


Solution
--------

First of all, I've tried to execute it:

.. code-block:: shell-session

   $ ./dMd
   Enter the valid key!
   foobar
   Invalid Key! :(

I need to reverse the right password..

To disassemble a function you can run:

.. code-block:: shell-session

   $ gdb ./dMd -batch -ex 'disassemble main' | c++filt

*(the program* ``c++filt`` *just demangles C++ symbols)*

Let's take a look at the disassembled code..

The first part **asks for the password** and stores the input in a string pointed by the register ``rax``:

.. code-block:: c-objdump

   0x0000000000400e8d <+0>:	push   rbp
   0x0000000000400e8e <+1>:	mov    rbp,rsp
   0x0000000000400e91 <+4>:	push   rbx
   0x0000000000400e92 <+5>:	sub    rsp,0x78
   0x0000000000400e96 <+9>:	mov    rax,QWORD PTR fs:0x28
   0x0000000000400e9f <+18>:	mov    QWORD PTR [rbp-0x18],rax
   0x0000000000400ea3 <+22>:	xor    eax,eax
   0x0000000000400ea5 <+24>:	mov    esi,0x4028a8
   0x0000000000400eaa <+29>:	mov    edi,0x604260
   0x0000000000400eaf <+34>:	call   0x400cc0 <std::basic_ostream<char, std::char_traits<char> >& std::operator<< <std::char_traits<char> >(std::basic_ostream<char, std::char_traits<char> >&, char const*)@plt>
   0x0000000000400eb4 <+39>:	lea    rax,[rbp-0x50]
   0x0000000000400eb8 <+43>:	mov    rsi,rax
   0x0000000000400ebb <+46>:	mov    edi,0x604140
   0x0000000000400ec0 <+51>:	call   0x400d00 <std::basic_istream<char, std::char_traits<char> >& std::operator>><char, std::char_traits<char> >(std::basic_istream<char, std::char_traits<char> >&, char*)@plt>
   0x0000000000400ec5 <+56>:	lea    rax,[rbp-0x71]
   0x0000000000400ec9 <+60>:	mov    rdi,rax
   0x0000000000400ecc <+63>:	call   0x400d60 <std::allocator<char>::allocator()@plt>
   0x0000000000400ed1 <+68>:	lea    rdx,[rbp-0x71]
   0x0000000000400ed5 <+72>:	lea    rcx,[rbp-0x50]
   0x0000000000400ed9 <+76>:	lea    rax,[rbp-0x70]
   0x0000000000400edd <+80>:	mov    rsi,rcx
   0x0000000000400ee0 <+83>:	mov    rdi,rax
   0x0000000000400ee3 <+86>:	call   0x400cf0 <std::basic_string<char, std::char_traits<char>, std::allocator<char> >::basic_string(char const*, std::allocator<char> const&)@plt>
   0x0000000000400ee8 <+91>:	lea    rax,[rbp-0x60]
   0x0000000000400eec <+95>:	lea    rdx,[rbp-0x70]
   0x0000000000400ef0 <+99>:	mov    rsi,rdx
   0x0000000000400ef3 <+102>:	mov    rdi,rax

Then it takes the input I provided and generates the ``md5``:

.. code-block:: cpp-objdump

   0x0000000000400ef6 <+105>:	call   0x402526 <md5(std::basic_string<char, std::char_traits<char>, std::allocator<char> >)>
   0x0000000000400efb <+110>:	lea    rax,[rbp-0x60]
   0x0000000000400eff <+114>:	mov    rdi,rax
   0x0000000000400f02 <+117>:	call   0x400c50 <std::basic_string<char, std::char_traits<char>, std::allocator<char> >::c_str() const@plt>
   0x0000000000400f07 <+122>:	mov    QWORD PTR [rbp-0x58],rax
   0x0000000000400f0b <+126>:	lea    rax,[rbp-0x60]
   0x0000000000400f0f <+130>:	mov    rdi,rax
   0x0000000000400f12 <+133>:	call   0x400cd0 <std::basic_string<char, std::char_traits<char>, std::allocator<char> >::~basic_string()@plt>
   0x0000000000400f17 <+138>:	lea    rax,[rbp-0x70]
   0x0000000000400f1b <+142>:	mov    rdi,rax
   0x0000000000400f1e <+145>:	call   0x400cd0 <std::basic_string<char, std::char_traits<char>, std::allocator<char> >::~basic_string()@plt>
   0x0000000000400f23 <+150>:	lea    rax,[rbp-0x71]
   0x0000000000400f27 <+154>:	mov    rdi,rax
   0x0000000000400f2a <+157>:	call   0x400d30 <std::allocator<char>::~allocator()@plt>

Then it checks if the input is correct..

There are a lot of similar code snippets, following the same pattern:

.. uml::

   start
   :tmp = rax;
   repeat
     :rax = tmp;
     :Consider rax[index];
     if (rax[index] != expected byte) then (yes)
       #Red:Error;
       stop
     endif
     :index += 1;
   repeat while (index < password.length)
   stop

Each code snippet is like:

.. code-block:: cpp-objdump

   0x0000000000400f3e <+177>:	mov    rax,QWORD PTR [rbp-0x58]  // rax = tmp
   0x0000000000400f42 <+181>:	add    rax,0x1                   // rax[1]
   0x0000000000400f46 <+185>:	movzx  eax,BYTE PTR [rax]
   0x0000000000400f49 <+188>:	cmp    al,0x38                   // check if rax[1] == 0x38
   0x0000000000400f4b <+190>:	jne    0x40129b <main+1038>      // otherwise print error and exit

The bytes used in comparisons are:

+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
| 7 | 8 | 0 | 4 | 3 | 8 | d | 5 | b | 6 | e | 2 | 9 | d | b | 0 | 8 | 9 | 8 | b | c | 4 | f | 0 | 2 | 2 | 5 | 9 | 3 | 5 | c | 0 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+

This means the *md5 of the password* must be: ``780438d5b6e29db0898bc4f0225935c0``.

I just need to reverse that string and I've got the password.

`Checking online`_ for the *reverse that md5*, I've found:

.. code-block:: text

   b781cbb29054db12f88f08c6e161c199

that is the flag.

.. _`Checking online`: http://md5.gromweb.com/?md5=780438d5b6e29db0898bc4f0225935c0
