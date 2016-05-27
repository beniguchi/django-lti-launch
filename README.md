# Django LTI Launch App

This repository contains a reusable Django app `ltilaunch` to manage user authorization via LTI 1.x.
It also contains a test Django project `django_lti_launch` to use for development and as a basic example of usage.

## Development Environment Setup

These steps are only needed if you wish to work with the `ltilaunch` app in the context of the testing-only `django_lti_launch` project.  Use a [prebuilt package](#build-package) and `pip` to make use of the app in a production Django project.

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

## Build App Package
<a name="build-package"></a>

To avoid micromanaging developer-hosted Python versions, the `remote_build.sh` script uses the Vagrant VM to create the distribution files.  A build server could use the `build.sh` script directly.  Either way, running

```
$ ./dev_scripts/remote_build.sh
```

or

```
$ ./dev_scripts/build.sh
```

should result in a `dist/` directory containing the needed artifacts.
