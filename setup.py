import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pycti-arbin",
    version="0.0.3",
    author="Zander Nevitt",
    author_email="zandern@battgenie.life",
    description="A class based Python interface for communication and control of Arbin cyclers over CTI.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BattGenie/pycti.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)