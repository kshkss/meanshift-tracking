from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

#with open('meanshift/__init__.py') as f:
    #text = f.read()

#version = re.search("__version__ = '(.*?)'", text).groups()[0]

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

ext_modules = [
        Extension("meanshift", sources = ["src/histogram.cpp", "src/meanshift.pyx"])
        ]

setup(
    #version=version,
    # You can just specify package directories manually here if your project is
    # simple. Or you can use find_packages().
    #
    # Alternatively, if you just want to distribute a single Python file, use
    # the `py_modules` argument instead as follows, which will expect a file
    # called `my_module.py` to exist:
    #
    #   py_modules=["my_module"],
    #
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    python_requires='>=3.7, <4',

    install_requires=['numpy>=1.17'],

    #ext_modules=cythonize("src/histogram.cpp", "src/meanshift.pyx"),
    ext_modules=cythonize(ext_modules),
)

