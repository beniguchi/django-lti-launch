#!/bin/sh

PY3=/home/vagrant/.virtualenvs/django-lti-launch/bin/python3
vagrant ssh -c \
    "cd /vagrant/django_lti_launch && ${PY3} ./manage.py $*"
