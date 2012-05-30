import os.path
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from plastic.version import VERSION


def readme():
    try:
        with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
            return f.read()
    except (IOError, OSError):
        return ''


setup(
    name='Plastic',
    packages=['plastic', 'plastictests'],
    version=VERSION,
    description='Web framework built on top of Werkzeug',
    long_description=readme(),
    license='MIT License',
    author='Hong Minhee',
    author_email='minhee' '@' 'dahlia.kr',
    maintainer='Hong Minhee',
    maintainer_email='minhee' '@' 'dahlia.kr',
    url='https://bitbucket.org/dahlia/plastic',
    install_requires=['Werkzeug >= 0.8', 'distribute'],
    tests_require=['Attest'],
    test_loader='attest:auto_reporter.test_loader',
    test_suite='plastictests.tests',
    extras_require={'docs': ['Sphinx >= 1.1']},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
