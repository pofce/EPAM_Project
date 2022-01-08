from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='EPAM_Project',
    version='1.0.0.',
    packages=['department_app', 'department_app.rest', 'department_app.forms',
              'department_app.tests',
              'department_app.views', 'department_app.errors', 'department_app.models',
              'department_app.service'],
    url='https://github.com/pofce/EPAM_Project',
    author='Vladyslav Radchenko',
    author_email=' vladyslav.radchenko.ki.2019@lpnu.ua ',
    description=long_description,
    include_package_data=True,
    zip_safe=False,
)
