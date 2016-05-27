import os
from setuptools import find_packages, setup


PROJECT_PATH = os.path.dirname(__file__)
with open(os.path.join(PROJECT_PATH, "requirements", "base.txt")) as reqs:
    REQS = list(s.rstrip() for s in reqs.readlines())

# allow setup.py to be run from any path
os.chdir(
    os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-lti-launch',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='http://www.apache.org/licenses/LICENSE-2.0',
    description='IMS LTI launch authentication for Django',
    long_description="TODO",
    url="https://github.com/unizin/django-lti-launch",
    author="Unizin, Ltd.",
    author_email="dev@unizin.org",
    install_requires=REQS,
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 1.9",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5"
        "Topic :: Internet :: WWW/HTTP",
        "Development Status :: 3 - Alpha"
    ]
)