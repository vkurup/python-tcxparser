from setuptools import find_packages, setup

__version__ = "2.2.0"

setup(
    name="python-tcxparser",
    version=__version__,
    description="Simple parser for Garmin TCX files",
    long_description=open("README.rst").read(),
    author="Vinod Kurup",
    author_email="vinod@kurup.com",
    url="https://github.com/vkurup/python-tcxparser/",
    packages=find_packages(include=["tcxparser"]),
    include_package_data=True,
    license="BSD",
    zip_safe=False,
    keywords="tcx",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=[
        "lxml",
        "python-dateutil",
    ],
    test_suite="tests",
)
