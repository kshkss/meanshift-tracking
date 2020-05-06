from setuptools import setup, find_packages, Extension

setup(
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data = True,
    package_data = {'': ['libmeanshift.so', 'Meanshift.dll']},
    scripts=['scripts/drift'],
    python_requires='>=3.6, <4',
    install_requires=['numpy>=1.17', 'tifffile'],
)

