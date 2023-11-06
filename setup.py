from setuptools import find_packages, setup

setup(
    name='humanitarian_management_system',
    version='1.0.0',
    # Look for the packages in the current directory
    packages=find_packages(),
    # Specify the dependencies
    install_requires=[
        'numpy',
        'pandas',
    ],
    # Specify the entry points
    # A command is created for users to run the application
    entry_points={
        'console_scripts': [
            f'hmsGroup11={find_packages()[0]}.main:main',
        ],
    }
)
