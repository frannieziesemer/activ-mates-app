from flask import Flask, render_template, url_for
from app import app

"""A one line summary of the module or program, terminated by a period.

check here for a guide to documentation https://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings
Leave one blank line.  The rest of this docstring should contain an
overall description of the module or program.  Optionally, it may also
contain a brief description of exported classes and functions and/or usage
examples.

  Typical usage example:

  foo = ClassFoo()
  bar = foo.FunctionBar()
"""
# testing


def func(x):
    return x + 1


def test_answer():
    assert func(3) == 4


@app.route('/')
def index():
    return render_template('index.html')
