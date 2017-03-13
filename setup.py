try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import versioneer

setup(
    name='vlfeat-ctypes',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author='Dougal J. Sutherland',
    author_email='dougal@gmail.com',
    packages=['vlfeat'],
    url='https://github.com/dougalsutherland/vlfeat-ctypes',
    description='A minimal ctypes-based port of some vlfeat functions.',
    long_description=open('README.rst').read(),
    license='BSD',
    zip_safe=False,
    install_requires = ['numpy'],
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
