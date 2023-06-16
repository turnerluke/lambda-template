from setuptools import setup, find_packages
setup(
    name='lambda-template',
    version='0.0',
    author='Turner Luke',
    author_email='turnermluke@gmail.com',
    description='A template for AWS Lambda functions.',
    url='https://github.com/turnerluke/lambda-template',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    extras_require=dict(tests=['pytest']),
)