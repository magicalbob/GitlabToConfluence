from setuptools import setup

setup(
    name='gitlab_to_confluence',
    version='1.0.0',
    py_modules=['GitlabToConfluence'],
    install_requires=[
        'requests',
        'markdown',
        'atlassian',
    ],
)

