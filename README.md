# Django LTI Launch App

This repository contains a reusable Django app named `ltilaunch` to manage user authorization via LTI 1.x.
It also contains a test Django project `django_lti_launch` to use for development and as a basic example of usage.

## Installation

The development branch can be installed via `pip`:

```
$ pip install git+ssh://github.com/unizin/django-lti-launch
```

## Requirements

The `ltilaunch` app currently only works with the `postgresql_psycopg2` database backend.
It requires at least PostgreSQL 9.4 and at least Psycopg2 2.5.4.
See the [Postgres specific model fields](https://docs.djangoproject.com/en/1.9/ref/contrib/postgres/fields/) section of the Django documentation for more information.

## Configuration

In order to use the LTI launch functionality, you must add the `ltilaunch` app to your `settings.py` file:

```
INSTALLED_APPS = [
    # ...
    'ltilaunch',
    # ...
]
```

The app also installs an authentication backend to validate signed LTI launch requests.
This authentication backend depends on the standard Django user model, so both backends must be present in `settings.py`:

```
AUTHENTICATION_BACKENDS = [
    'ltilaunch.auth.LTILaunchBackend',
    'django.contrib.auth.backends.ModelBackend'],
    # ...
]
```

To create the tables necessary to track LTI logins, run `manage.py migrate ltilaunch` after making changes to your project settings.

## How to Use

[IMS Global LTI](https://www.imsglobal.org/specs/ltiv1p2/implementation-guide) specifies an authentication mechanism that relies on an out-of-band shared key and secret between a tool consumer and a tool provider.
This app provides a mechanism to manage this credential exchange in the Django admin site.

Before any LTI launch will succeed, you must create at least one `LTIConsumer` model object. This represents an external system that will use the LTI tool provided by your Django project.
This app's Django admin site form for LTI consumers will generate an `oauth_consumer_key` and `oauth_consumer_secret` value that must be shared with the LTI tool consumer's administrator.
You can optionally specify a `tool_consumer_instance_guid` value that the LTI tool consumer's administrator should be able to give to you.
Combined with selecting the _Match GUID and OAuth consumer_ option in the Django admin form, this value minimizes the potential impact of accidental OAuth credential misconfiguration—for example, a testing LMS instance won't be able to corrupt data for a production LMS instance by using the same key and secret.




## Development Environment Setup

These steps are only needed if you wish to work with the `ltilaunch` app in the context of the testing-only `django_lti_launch` project.

```
$ vagrant up
$ ./dev_scripts/remote_manage.sh migrate
$ ./dev_scripts/remote_manage.sh createsuperuser --username admin
```

Enter whatever you like for the superuser credentials.  Then:

```
$ ./dev_scripts/remote_manage.sh runsslserver 0.0.0.0:8000
```

The SSL devserver is used here to make it easy to use the Canvas LTI self-guided learning module without installing or managing extra web server software.  Production deploys should naturally use the Apache, nginx, ELB, or other frontend to provide SSL.

You should be able to access the Django admin UI at https://localhost:8000/admin/.  If this doesn't work, check that Vagrant did not assign a different port due to a collision with an existing service on the host machine.

