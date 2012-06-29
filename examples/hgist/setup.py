try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='Hgist',
    packages=['hgist'],
    include_package_data=True,
    package_data={'hgist': ['templates/*.html']},
    version='20120630',
    description='Gist clone, but powered by Mercurial',
    license='MIT License',
    author='Hong Minhee',
    author_email='minhee' '@' 'dahlia.kr',
    install_requires=['Mercurial', 'Plastic', 'Pygments']
)

