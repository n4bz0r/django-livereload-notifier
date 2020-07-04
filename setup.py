import setuptools


setuptools.setup(
    name                 = 'django-livereload-notifier',
    keywords             = 'django, development, server, runserver, livereload',
    description          = 'LiveReload with the Django development server',
    long_description     = open('README.md').read(),
    author               = 'n4bz0r',
    author_email         = 'n4bz0r.dev@gmail.com',
    version              = '0.1',
    license              = 'MIT License',
    url                  = 'https://github.com/n4bz0r/django-livereload-notifier',
    
    include_package_data = True,
    packages             = setuptools.find_packages(),
    
    classifiers = [
        'Framework :: Django',
        'Environment :: Web Environment',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    install_requires = [
        'beautifulsoup4>=4.3.2',
        'watchdog>=0.10.3',
    ],
)