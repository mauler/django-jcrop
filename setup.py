import os
from distutils.core import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='django-jcrop',
    version='0.1',
    description='Django app providing cropping functionnality with jcrop',
    author='Mathieu Comandon',
    author_email='strider@strycore.com',
    url='https://github.com/strycore/django-jcrop',
    packages=['django_jcrop'],
    license='BSD',
    long_description=read('README'),
    install_requires=[
        'easy_thumbnails',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Topic :: Utilities'
        'Environment :: Web Environment',
        'Framework :: Django',
    ],
)
