from setuptools import find_packages, setup


def get_devtools_packages():
    return [f"snowflake.{pkg}" for pkg in find_packages(where="src/snowflake")]


print(get_devtools_packages())


setup(
    name='snowpark-python-devtools',
    version='0.1.0',
    license="Apache License, Version 2.0",
    description='Snowflake Snowpark Python DevTools',
    packages=get_devtools_packages(),
    package_dir={
        "": "src",
    },
    python_requires=">=3.7",
    install_requires=[
        "PyYAML",
        "wrapt",
        "six>=1.5",
        "yarl",
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        "Programming Language :: Python :: 3 :: Only",
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        "License :: OSI Approved :: Apache Software License",
    ],
    entry_points={
        'pytest11': [
            'snowpark-python-devtools = snowflake.devtools.snowpark_pytest_plugin',
        ],
    },
)