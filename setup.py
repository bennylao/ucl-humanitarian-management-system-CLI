from setuptools import setup, find_namespace_packages

setup(
    name='humanitarian_management_system',
    version='1.0.0',
    install_requires=[
        "pandas~=2.1.3",
        "numpy~=1.22.0",
        "dash~=2.14.1",
        "plotly~=5.18.0",
        "tabulate"
    ],
    packages=find_namespace_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'hmsGroup11 = humanitarian_management_system.main:main',
        ]
    }
)