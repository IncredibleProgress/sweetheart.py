# Learn Python

## Table of content

<!-- toc -->

## Basics

### Python within a terminal

Within any terminal copy the following command and press the `RETURN` key for starting the sweetheart python shell. Using WSL (Windows Subsystem for Linux) it works within PowerShell or Cmd. Within Ubuntu terminal the `bash` command is not required.

```sh
bash sweet shell python
```

It will start the following prompt ready for coding in python. It will allow you to make first steps and experiments with this amazing programming language.

```sh
[SWEETHEART] shell$ /opt/sweetheart/programs/envPy/bin/ipython3
Python 3.8.5 (default, Jul 28 2020, 12:59:40)
Type 'copyright', 'credits' or 'license' for more information
IPython 7.19.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]:
```

### A first welcome message

Now type `import __hello__` and then press the `RETURN` key. Afterwards try `print("welcome!")` and `RETURN`. If the following lines happend, congratulations that means these are your first successfull lines of python!

```python
In [1]: import __hello__
Hello world!

In [2]: print("welcome!")
welcome!
```

Let's make some comments, we already did a lot with such minimalistic examples. The `import` keyword is what we call a *reserved keyword* because you cannot use it for your own purpose. It allows you to import any existing and available *python modules* for loading it and using it within your programs. `__hello__` is one of the *built-in* modules. That means a module integrated within python itself.

Now let's talk about `print()`. This is what is named a *function*. The functions are more or less what is the most important *objects* within any languages! Note that we always *call* a function using brakets `()`. This is how we know and how python knows we are calling a function. Typing simply `print()` runs but will print nothing because no *arguments* are provided into the brakets `()`.

Look at `"welcome!"`, this is the *argument* given to the *function* `print()` within previous instruction `print("welcome!")`. This is too what is named a *string*. We can recognize it with the use of delimiters `""` which creates a string *object*. A *string* is nothing else that a set of alphanumerical characters stored in memory to be computed later. Alternatively we can use the `'` delimiter instead of `"`. It allows nested capabilities like follow. It works reversely.

```python
In [3]: print('I am a "nested string" which can help')
I am a "nested string" which can help
```

### Fundamental objects

#### String

```py
>>> a = "Hello Python"
>>> l = list(a)
>>> l[0], l[6] = 'h', 'p'
>>> ''.join(l)
'hello python'
```

#### Numbers

#### List

Lists are versatile containers. Python provides a lot of ways such as
**negative index**, **slicing statement**, or **list comprehension** to
manipulate lists. The following snippet shows some common operations of lists.

```py
>>> a = [1, 2, 3, 4, 5]
>>> a[-1]                     # negative index
5
>>> a[1:]                     # slicing
[2, 3, 4, 5]
>>> a[1:-1]
[2, 3, 4]
>>> a[1:-1:2]
[2, 4]
>>> a[::-1]                   # reverse
[5, 4, 3, 2, 1]
>>> a[0] = 0                  # set an item
>>> a
[0, 2, 3, 4, 5]
>>> a.append(6)               # append an item
>>> a
[0, 2, 3, 4, 5, 6]
>>> del a[-1]                 # del an item
>>> a
[0, 2, 3, 4, 5]
>>> b = [x for x in range(3)] # list comprehension
>>> b
[0, 1, 2]
>>> a + b                     # add two lists
[0, 2, 3, 4, 5, 0, 1, 2]
```

#### Dict

Dictionaries are key-value pairs containers. Like lists, Python supports many
ways such as **dict comprehensions** to manipulate dictionaries. After
Python 3.6, dictionaries preserve the insertion order of keys. The Following
snippet shows some common operations of dictionaries.

    >>> d = {'timmy': 'red', 'barry': 'green', 'guido': 'blue'}
    >>> d
    {'timmy': 'red', 'barry': 'green', 'guido': 'blue'}
    >>> d['timmy'] = "yellow"        # set data
    >>> d
    {'timmy': 'yellow', 'barry': 'green', 'guido': 'blue'}
    >>> del d['guido']               # del data
    >>> d
    >>> 'guido' in d                 # contain data
    False
    {'timmy': 'yellow', 'barry': 'green'}
    >>> {k: v for k ,v in d.items()} # dict comprehension
    {'timmy': 'yellow', 'barry': 'green'}
    >>> d.keys()                     # list all keys
    dict_keys(['timmy', 'barry'])
    >>> d.values()                   # list all values
    dict_values(['yellow', 'green'])

#### collection

### Functions

Defining a function in Python is flexible. We can define a function with
**function documents**, **default values**, **arbitrary arguments**,
**keyword arguments**, **keyword-only arguments**, and so on. The Following
snippet shows some common expressions to define functions.

.. code-block:: python

    def foo_with_doc():
        """Documentation String."""

    def foo_with_arg(arg): ...
    def foo_with_args(*arg): ...
    def foo_with_kwarg(a, b="foo"): ...
    def foo_with_args_kwargs(*args, **kwargs): ...
    def foo_with_kwonly(a, b, *, k): ...           # python3
    def foo_with_annotations(a: int) -> int: ...   # python3

Function Annotations
--------------------

Instead of writing string documents in functions to hint the type of parameters
and return values, we can denote types by **function annotations**. Function annotations
which the details can be found on PEP `3017 <https://www.python.org/dev/peps/pep-3107>`_
and PEP `484 <https://www.python.org/dev/peps/pep-0484/>`_ were introduced in
Python 3.0. They are an **optional** feature in **Python 3**. Using function
annotations will lose compatibility in **Python 2**. We can solve this issue
by stub files. In addition, we can do static type checking through
`mypy <http://mypy-lang.org/>`_.

```py
>>> def fib(n: int) -> int:
...     a, b = 0, 1
...     for _ in range(n):
...         b, a = a + b, b
...     return a
...
>>> fib(10)
55


>>> import sys
>>> print(sys.version)
3.7.1 (default, Nov  6 2018, 18:46:03)
[Clang 10.0.0 (clang-1000.11.45.5)]



>>> import platform
>>> platform.python_version()
'3.7.1'



>>> import sys
>>> sys.version_info >= (3, 6)
True
>>> sys.version_info >= (3, 7)
False
```

#### advanced functions type

##### iterator

##### generator

##### decorator

Ellipsis
--------

`Ellipsis <https://docs.python.org/3/library/constants.html#Ellipsis>`_ is a
built-in constant. After Python 3.0, we case use ``...`` as ``Ellipsis``. It
may be the most enigmatic constant in Python. Based on the official document,
we can use it to extend slicing syntax. Nevertheless, there are some other
conventions in type hinting, stub files, or function expressions.

.. code-block:: python

    >>> ...
    Ellipsis
    >>> ... == Ellipsis
    True
    >>> type(...)
    <class 'ellipsis'>

The following snippet shows that we can use the ellipsis to represent a function
or a class which has not implemented yet.

.. code-block:: python

    >>> class Foo: ...
    ...
    >>> def foo(): ...
    ...

if ... elif ... else
--------------------

The **if statements** are used to control the code flow. Instead of using
``switch`` or ``case`` statements control the logic of the code, Python uses
``if ... elif ... else`` sequence. Although someone proposes we can use
``dict`` to achieve ``switch`` statements, this solution may introduce
unnecessary overhead such as creating disposable dictionaries and undermine
a readable code. Thus, the solution is not recommended.

.. code-block:: python

    >>> import random
    >>> num = random.randint(0, 10)
    >>> if num < 3:
    ...     print("less than 3")
    ... elif num < 5:
    ...     print("less than 5")
    ... else:
    ...     print(num)
    ...
    less than 3

for Loop
--------

In Python, we can access iterable object's items directly through the
**for statement**. If we need to get indexes and items of an iterable object
such as list or tuple at the same time, using ``enumerate`` is better than
``range(len(iterable))``. Further information can be found on
`Looping Techniques <https://docs.python.org/3/tutorial/datastructures.html#looping-techniques>`_.

.. code-block:: python

    >>> for val in ["foo", "bar"]:
    ...     print(val)
    ...
    foo
    bar
    >>> for idx, val in enumerate(["foo", "bar", "baz"]):
    ...     print(idx, val)
    ...
    (0, 'foo')
    (1, 'bar')
    (2, 'baz')

for ... else ...
----------------

It may be a little weired when we see the ``else`` belongs to a ``for`` loop at
the first time. The ``else`` clause can assist us to avoid using flag
variables in loops. A loop’s ``else`` clause runs when no break occurs.

.. code-block:: python

    >>> for _ in range(5):
    ...     pass
    ... else:
    ...     print("no break")
    ...
    no break

The following snippet shows the difference between using a flag variable and
the ``else`` clause to control the loop. We can see that the ``else`` does not
run when the ``break`` occurs in the loop.

.. code-block:: python

    >>> is_break = False
    >>> for x in range(5):
    ...     if x % 2 == 0:
    ...         is_break = True
    ...         break
    ...
    >>> if is_break:
    ...     print("break")
    ...
    break

    >>> for x in range(5):
    ...     if x % 2 == 0:
    ...         print("break")
    ...         break
    ... else:
    ...     print("no break")
    ...
    break

Using ``range``
---------------

The problem of ``range`` in Python 2 is that ``range`` may take up a lot of
memory if we need to iterate a loop many times. Consequently, using ``xrange``
is recommended in Python 2.

.. code-block:: python

    >>> import platform
    >>> import sys
    >>> platform.python_version()
    '2.7.15'
    >>> sys.getsizeof(range(100000000))
    800000072
    >>> sys.getsizeof(xrange(100000000))
    40

In Python 3, the built-in function ``range`` returns an iterable **range object**
instead of a list. The behavior of ``range`` is the same as the ``xrange`` in
Python 2. Therefore, using ``range`` do not take up huge memory anymore if we
want to run a code block many times within a loop. Further information can be
found on PEP `3100 <https://www.python.org/dev/peps/pep-3100>`_.

.. code-block:: python

    >>> import platform
    >>> import sys
    >>> platform.python_version()
    '3.7.1'
    >>> sys.getsizeof(range(100000000))
    48

while ... else ...
------------------

The ``else`` clause belongs to a while loop serves the same purpose as the
``else`` clause in a for loop. We can observe that the ``else`` does not run
when the ``break`` occurs in the while loop.

.. code-block:: python

    >>> n = 0
    >>> while n < 5:
    ...     if n == 3:
    ...         break
    ...     n += 1
    ... else:
    ...     print("no break")
    ...

The ``do while`` Statement
--------------------------

There are many programming languages such as C/C++, Ruby, or Javascript,
provide the ``do while`` statement. In Python, there is no ``do while``
statement. However, we can place the condition and the ``break`` at the end of
a ``while`` loop to achieve the same thing.

.. code-block:: python

    >>> n = 0
    >>> while True:
    ...     n += 1
    ...     if n == 5:
    ...         break
    ...
    >>> n
    5

try ... except ... else ...
---------------------------

Most of the time, we handle errors in ``except`` clause and clean up resources
in ``finally`` clause. Interestingly, the ``try`` statement also provides an
``else`` clause for us to avoid catching an exception which was raised by the
code that should not be protected by ``try ... except``. The ``else`` clause
runs when no exception occurs between ``try`` and ``except``.

.. code-block:: python

    >>> try:
    ...     print("No exception")
    ... except:
    ...     pass
    ... else:
    ...     print("Success")
    ...
    No exception
    Success


Generators
----------

Python uses the ``yield`` statement to define a **generator function**. In
other words, when we call a generator function, the generator function will
return a **generator** instead of return values for creating an **iterator**.

.. code-block:: python

    >>> def fib(n):
    ...     a, b = 0, 1
    ...     for _ in range(n):
    ...         yield a
    ...         b, a = a + b, b
    ...
    >>> g = fib(10)
    >>> g
    <generator object fib at 0x10b240c78>
    >>> for f in fib(5):
    ...     print(f)
    ...
    0
    1
    1
    2
    3

Generator Delegation
--------------------

Python 3.3 introduced ``yield from`` expression. It allows a generator to
delegate parts of operations to another generator. In other words, we can
**yield** a sequence **from** other **generators** in the current **generator function**.
Further information can be found on PEP `380 <https://www.python.org/dev/peps/pep-0380>`_.

.. code-block:: python

    >>> def fib(n):
    ...     a, b = 0, 1
    ...     for _ in range(n):
    ...         yield a
    ...         b, a = a + b, b
    ...
    >>> def fibonacci(n):
    ...     yield from fib(n)
    ...
    >>> [f for f in fibonacci(5)]
    [0, 1, 1, 2, 3]

Class
-----

Python supports many common features such as **class documents**, **multiple inheritance**,
**class variables**, **instance variables**, **static method**, **class method**, and so on.
Furthermore, Python provides some special methods for programmers to implement
**iterators**, **context manager**, etc. The following snippet displays common definition
of a class.

.. code-block:: python

    class A: ...
    class B: ...
    class Foo(A, B):
        """A class document."""

        foo = "class variable"

        def __init__(self, v):
            self.attr = v
            self.__private = "private var"

        @staticmethod
        def bar_static_method(): ...

        @classmethod
        def bar_class_method(cls): ...

        def bar(self):
            """A method document."""

        def bar_with_arg(self, arg): ...
        def bar_with_args(self, *args): ...
        def bar_with_kwarg(self, kwarg="bar"): ...
        def bar_with_args_kwargs(self, *args, **kwargs): ...
        def bar_with_kwonly(self, *, k): ...
        def bar_with_annotations(self, a: int): ...

``async`` / ``await``
---------------------

``async`` and ``await`` syntax was introduced from Python 3.5. They were
designed to be used with an event loop. Some other features such as the
**asynchronous generator**  were implemented in later versions.

A **coroutine function**
(``async def``) are used to create a **coroutine** for an event loop. Python
provides a built-in module, **asyncio**, to write a concurrent code through
``async``/``await`` syntax. The following snippet shows a simple example of
using **asyncio**. The code must be run on Python 3.7 or above.

.. code-block:: python

    import asyncio

    async def http_ok(r, w):
        head = b"HTTP/1.1 200 OK\r\n"
        head += b"Content-Type: text/html\r\n"
        head += b"\r\n"

        body = b"<html>"
        body += b"<body><h1>Hello world!</h1></body>"
        body += b"</html>"

        _ = await r.read(1024)
        w.write(head + body)
        await w.drain()
        w.close()

    async def main():
        server = await asyncio.start_server(
            http_ok, "127.0.0.1", 8888
        )

        async with server:
            await server.serve_forever()

    asyncio.run(main())

Avoid ``exec`` and ``eval``
---------------------------

The following snippet shows how to use the built-in function ``exec``. Yet,
using ``exec`` and ``eval`` are not recommended because of some security issues
and unreadable code for a human. Further reading can be found on
`Be careful with exec and eval in Python <http://lucumr.pocoo.org/2011/2/1/exec-in-python/>`_
and `Eval really is dangerous <https://nedbatchelder.com/blog/201206/eval_really_is_dangerous.html>`_


.. code-block:: python

    >>> py = '''
    ... def fib(n):
    ...     a, b = 0, 1
    ...     for _ in range(n):
    ...         b, a = b + a, b
    ...     return a
    ... print(fib(10))
    ... '''
    >>> exec(py, globals(), locals())
    55