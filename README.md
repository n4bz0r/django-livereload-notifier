# Django-livereload-notifier

## About

`Django-livereload-notifier` is an application that substitutes Django `runserver` command
with the one that keeps track of template files changes, and sends a request to a livereload
server when files in those directories are modified or when development server is restarted.

There is also a convenient middleweare that injects livereload `<script>` tag into all pages.

The client-side script should be provided by livereload server (it usually is).

## Features

- **Livereload server notification on template files changes**
- Livereload server notification on development server restart
- Middleware for injecting livereload `<script>` tags

## Alternatives

- <https://github.com/tjwalch/django-livereload-server>
- <https://github.com/Fantomas42/django-livereload>

## Reasoning

Before making my own thing, I tried similar solutions, but they didn't work exactly as I 
expected:

- specified in settings livereload server host and port weren't used in script injecting
 middleware making it impossible to connect from a different device
- static file changes weren't registered by livereload server sometimes
- directories specified in command-line options weren't watched by livereload server
- template changes weren't watched

Tired of tinkering with existing solutions to no avail, I looked into the source
code of [Fantomas42's solution](https://github.com/Fantomas42/django-livereload), 
and ended up rewriting the entire thing to my liking.

## Installation

### Requirements

- Python 3.6+ (mostly because of `f-strings`). Open an issue if you think an older
  version should really be supported
- Django 2+

### Package installation

```bash
pip install git+https://github.com/n4bz0r/django-livereload-notifier.git
```

The package is not yet available on PyPi.

### Registering the application

Add `livereload.django` application to Django `INSTALLED_APPS` setting.

### Registering the script injecting middleware

Add `livereload.django.middleware.LiveReloadScriptInjector` to Django `MIDDLEWARE` setting 
before the `django.contrib.staticfiles` (if used).

### Running

Simply use `manage.py runserver` like you usually would. List of available options you can
find in the following section.

## Configuration

### Settings

- `LIVERELOAD_HOST` — livereload server host. Default: `'localhost'`
- `LIVERELOAD_PORT` — livereload server port. Default: `35729`

### Command-line options

- `--livereload-host` — livereload server host. Overrides `LIVERELOAD_HOST` setting if specified
- `--livereload-port` — livereload server port. Overrides `LIVERELOAD_PORT` setting if specified

## Links

### Livereload server implementations

- <https://github.com/vohof/gulp-livereload> (gulp plugin, that's what I use)
- <https://github.com/lepture/python-livereload> (python)
- <https://github.com/mklabs/tiny-lr> (nodejs)

### Thanks

- [Fantomas42](https://github.com/Fantomas42) for providing [a solid point of reference](https://github.com/Fantomas42/django-livereload)