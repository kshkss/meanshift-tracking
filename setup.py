from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize

ext_modules = [
        Extension("meanshift",
            sources=["src/histogram.cpp", "src/meanshift.pyx"],
            extra_compile_args=['-O3'])
        ]

setup(
    packages=find_packages('src'),
    package_dir={'': 'src'},
    ext_modules=cythonize(ext_modules, compiler_directives={'language_level':'3'}),
    py_modules=['meanshift_version'],
    scripts=['scripts/rotation-center', 'scripts/drift'],
    python_requires='>=3.6, <4',
    install_requires=['numpy>=1.17', 'Cython>=0.29', 'tifffile'],
)

