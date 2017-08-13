from setuptools import setup, find_packages


setup(
    name="multicore",
    description="Simpler Python multiprocess coding. Persistent workers, memory maps for minimum overhead.",
    long_description = open("README.rst", "r").read() + open("AUTHORS.rst", "r").read() + open("CHANGELOG.rst", "r").read(),
    version="0.1.1",
    author="Praekelt Consulting",
    author_email="dev@praekelt.com",
    license="BSD",
    url="http://github.com/praekelt/multicore",
    packages = find_packages(),
    dependency_links = [
    ],
    install_requires = [
        "dill"
    ],
    tests_require = [
        "tox",
    ],
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    zip_safe=False,
)
