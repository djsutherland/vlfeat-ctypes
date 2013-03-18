from numpy.distutils.core import setup

setup(
    name='vlfeat-ctypes',
    version='0.1.0dev',
    author='Dougal J. Sutherland',
    author_email='dougal@gmail.com',
    packages=['vlfeat'],
    url='https://github.com/dougalsutherland/vlfeat-ctypes',
    description='A minimal ctypes-based port of some vlfeat functions.',
    long_description=open('README.txt').read(),
)
