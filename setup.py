from setuptools import find_packages, setup

setup(
    name='pandora',
    version='1.0.0',
    url='https://sumsc.xin/pandora/2',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'test': [
            'pytest'
        ],
    },
)