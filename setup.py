from distutils.core import setup

setup(
    name='django-jcrop',
    version='0.1',
    description='Django app providing cropping functionnality with jcrop',
    author='Mathieu Comandon',
    author_email='strider@strycore.com',
    url='https://github.com/strycore/django-jcrop',
    packages=['django_jcrop'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Topic :: Utilities'
        'Environment :: Web Environment',
        'Framework :: Django',
    ],
)
