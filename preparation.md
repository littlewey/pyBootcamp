---
title: "Preparation"
date: 2018-02-09T19:41:55+08:00
weight: 0
draft: true
---

Slack channel: [#py-camp](https://project-inno.slack.com/messages/C8Z6GEF16)

### Environment setup

a Linux VM (Ubuntu) will do, reference: https://askubuntu.com/questions/142549/how-to-install-ubuntu-on-virtualbox

- 3G ram
- 1-2 CPU

### A just working editor

`Sublime text`/`Atom`/`VS code` will do the job, I was using `Sublime Text 3`

reference: http://tipsonubuntu.com/2017/05/30/install-sublime-text-3-ubuntu-16-04-official-way/

### How to run your python code?

**Preparation**:

to avoid anything stops you from the beginning let's just use python3 directly, if you know how to use `virtualenv`, use it instead, if you don't know `virtualenv` do it as below.

- install pip for python3, upgrade it then:

```bash
$ sudo apt-get install python3-pip -y
$ sudo pip3 install --upgrade pip
```

- install `ipython` as your python playground console

```bash
$ sudo pip3 install ipython
```

**Hello world!** from ipython

You could use it in one terminal for debugging for always, it's better than the python console in some ways.

```shell
$ ipython3
Python 3.5.2 (default, Nov 23 2017, 16:37:01)
Type 'copyright', 'credits' or 'license' for more information
IPython 6.2.1 -- An enhanced Interactive Python. Type '?' for help.

In [1]: print ("hello world!")
hello world!
In [2]: exit
$
```

**Hello world!** from your first python script

```shell
$ cat hello_world.py
print ("Hello world!")

$ python3 hello_world.py
Hello world!
```

Congratulations! One more step left:

### Go through the tutor

reference: https://docs.python.org/3/tutorial/

or: http://www.pythondoc.com/pythontutorial3/

