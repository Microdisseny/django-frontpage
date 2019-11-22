from setuptools import find_packages, setup

setup(
    name='django-frontpage',
    version='1.0.2',
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
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
