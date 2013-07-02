try:
    import numpy
except ImportError:
    raise ImportError("py-sdm requires numpy to be installed")
    # Don't do this in the setup() requirements, because otherwise pip and
    # friends get too eager about updating numpy.

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='vlfeat-ctypes',
    version='0.1.3',
    author='Dougal J. Sutherland',
    author_email='dougal@gmail.com',
    packages=['vlfeat'],
    url='https://github.com/dougalsutherland/vlfeat-ctypes',
    description='A minimal ctypes-based port of some vlfeat functions.',
    long_description=open('README.rst').read(),
    license='BSD',
    zip_safe=False,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 2 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Scientific/Engineering :: Image Recognition",
    ],
)
