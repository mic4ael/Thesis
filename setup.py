from setuptools import setup, find_packages

setup(
    name='imagepy',
    version='0.0.1',
    packages=find_packages('src'),
    test_suite='tests',
    package_dir={'': 'src'},
    install_requires=[
        'nose', 
        'mock', 
        'Pillow',
        'scipy',
    ]
)
