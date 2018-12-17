from setuptools import setup

setup(
    name='maxwell-api-client',
    version='0.1.0',
    author='Bas Wind',
    author_email='mailtobwind+mac@gmail.com',
    description='Maxwell API Client',
    url='https://bitbucket.org/maxwell/maxwell-api-client',
    packages=['maxwell'],
    install_requires=open('requirements.txt', 'r').readlines(),
    include_package_data=True,
    long_description=open('README.md').read(),
)
