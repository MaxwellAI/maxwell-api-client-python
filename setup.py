from setuptools import find_packages, setup

setup(
    name='maxwell-api-client',
    version='0.1.0',
    author='Bas Wind',
    author_email='mailtobwind+mac@gmail.com',
    description='Maxwell API Client',
    url='https://bitbucket.org/maxwellai/maxwell-api-client',
    packages=find_packages(),
    install_requires=['requests'],
    include_package_data=True,
    long_description=open('README.md').read(),
)
