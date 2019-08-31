from setuptools import setup
setup(
    name='kms-env',
    version='0.1.1',
    description="""Secrets Managemnt Config AWS""",
    long_description=open('README.md', 'r').read(),
    author='Alexander Beach',
    author_email='ajbeach2@gmail.com',
    url='https://github.com/ajbeach2/kms-env',
    packages=[
        'kms_env',
        'tests'
    ],
    install_requires=[
        'boto3>=1.9',
    ],
    test_suite='tests',
    setup_requires=['pytest-runner'],
    license="MIT",
    python_requires='>=3.7',
    keywords=('kms', 'ssm', 'secrets', 'aws'),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
    ],
)
