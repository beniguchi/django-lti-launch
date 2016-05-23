#!/bin/sh

PY3=/home/vagrant/.virtualenvs/django-lti-launch/bin/python3
vagrant ssh -c \
    "${PY3} /vagrant/django_lti_launch/manage.py migrate"
