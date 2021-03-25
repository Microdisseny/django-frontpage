from setuptools import find_packages, setup

CLASSIFIERS = [
    'Framework :: Django',
    'Framework :: Django :: 2.0',
    'Framework :: Django :: 2.1',
    'Framework :: Django :: 2.2',
    'Framework :: Django :: 3.0',
    'Framework :: Django :: 3.1',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Environment :: Web Environment',
    'Development Status :: 5 - Production/Stable',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

setup(
    name='django-frontpage',
    version='1.0.3',
    description='Show a page before your users authenticate into the admin site',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author='Microdisseny',
    author_email='tech@microdisseny.com',
    url='http://github.com/microdisseny/django-frontpage',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    classifiers=CLASSIFIERS
)
