# Django LTI Launch App

This repository contains a reusable Django app `ltilaunch` to manage user authorization via LTI 1.x.
It also contains a test Django project `django_lti_launch` to use for development and as a basic example of usage.

## Installation

The development branch can be installed via `pip`:

```
$ pip install git+ssh://github.com/unizin/django-lti-launch
```


## How to Use

TODO: describe needed changes to `settings.py`, provided admin functionality, and how to incorporate `LaunchView`


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

