import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

requires = [
    'django',
    'django-gravatar',
]
    
setup(
    name = "agile-django",
    version = "0.0.1",
    author = "Andres Torres",
    author_email = "andres.torres.marroquin@gmail.com",
    description = ("A agile"),
    license = "Internal",
    packages=['agile'],
    package_dir={'agile':'agile'},
    long_description=README,
    classifiers=[
    ],
    install_requires = requires,
    zip_safe = False,
)
