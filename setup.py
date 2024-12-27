from setuptools import setup, find_packages

setup(
    name="plane-py",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.8.0"
    ],
    author="Your Name",
    description="A Python client for the Plane API",
    python_requires=">=3.7",
)
