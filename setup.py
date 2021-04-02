from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="qwhale_logs_client",
    packages=["qwhale_logs_client"],
    include_package_data=True,
    version="v0.1.6",
    license="MIT",
    description="Python client for QwhaleLogs API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Yehoyada.s",
    author_email="hvuhsg6@gmail.com",
    url="https://logs.qwhale.ml",
    download_url="",
    keywords=[
        "API",
        "Client",
        "Qwhale",
        "QWhale",
        "client",
        "Logs",
        "log",
        "logs",
    ],  # Keywords that define your package best
    install_requires=["requests"],  # I get to this in a second
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",  # Define that your audience are developers
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",  # Again, pick a license
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
