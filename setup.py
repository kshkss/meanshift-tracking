from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize

ext_modules = [
        Extension("meanshift",
            sources=["src/histogram.cpp", "src/meanshift.pyx"],
            extra_compile_args=['-O3'])
        ]

setup(
    #packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    ext_modules=cythonize(ext_modules, compiler_directives={'language_level':'3'}),
    py_modules=['meanshift_version'],
    scripts=['scripts/rotation-center'],
    python_requires='>=3.7, <4',
    install_requires=['numpy>=1.17', 'Cython>=0.29'],
)

