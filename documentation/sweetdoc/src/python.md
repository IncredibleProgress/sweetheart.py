# Discover Python

## Basics

### Python within a terminal

Within any terminal copy the following command and press the `RETURN` key for starting the sweetheart python shell. Using *Windows Subsystem for Linux* it works within *PowerShell or Cmd. Within Ubuntu the `bash` command is not required.

``` bash
bash sws python
```

It will start the following prompt ready for making first steps and experiments in python.

```bash
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

Let's make some comments, we already did a lot with such minimalist example. The `import` keyword is what we call a *reserved keyword* because you cannot use it for your own purpose. It allows you to import any available *python modules* for loading it and using it within your programs. `__hello__` is one of the *built-in* modules. That means a module delivered within python itself.

Now let's talk about `print()`. This is what is named a *function*. A function is more or less the most important *object* within any languages. Note that we always *call* a function using brackets `()`. This is how we know and how python knows that we are calling a function. Typing simply `print()` runs but will print nothing because no *arguments* are provided into the brackets.

Look at `"welcome!"`, this is the *argument* given to the *function* `print()` within previous instruction `print("welcome!")`. This is too what is named a *string*. We can recognize it with the use of delimiters `""` which creates a string *object*. A *string* is nothing else that a set of alphanumerical characters which can be computed. Alternatively we can use the `'` delimiter instead of `"`. It allows nested capabilities like following (it works reversely too).

```python
In [3]: print('I am a "nested string" which can help')
I am a "nested string" which can help
```
