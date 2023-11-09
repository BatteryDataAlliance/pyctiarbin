import setuptools

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pycti-arbin",
    version="0.0.9",
    author="Zander Nevitt, Bing Syuan Wang",
    author_email="info@battgenie.life",
    description="A class based Python interface for communication and control of Arbin cyclers over CTI.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BattGenie/pycti.git",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
