from setuptools import find_packages, setup


setup(
    version='0.1.3',
    name='incuna-pagination',
    packages=find_packages(exclude=["test_project"]),
    include_package_data=True,
    install_requires=[],
    description='Utilities for paginated views.',
    author='Incuna Ltd',
    author_email='admin@incuna.com',
    url='https://github.com/incuna/incuna-pagination',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ],
)
