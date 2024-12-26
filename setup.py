from setuptools import setup, find_packages

setup(
    name="plane-py",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.8.0",
    ],
    author="vangauthic",
    author_email="heliumzeppelins@gmail.com",
    description="An async Python client for the Plane API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/vangauthic/plane-py/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
