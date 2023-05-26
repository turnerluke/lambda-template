from setuptools import setup, find_packages
setup(
    name='ziki-dbd-streams',
    version='0.0',
    author='Turner Luke',
    author_email='turnermluke@gmail.com',
    description='Data pipelines for ZIKI',
    url='https://github.com/turnerluke/ziki-dbd-streams',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    extras_require=dict(tests=['pytest']),
)