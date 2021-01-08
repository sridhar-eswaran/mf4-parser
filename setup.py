from setuptools import setup

with open('README.md') as fh:
	README = fh.read()


setup(
    name="mf4-parser",
    version="0.0.1",
    description="A Python package to extract signals from MDF4 files.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/sridhar-eswaran/mf4-parser.git",
    author="Sridhar Eswaran",
    author_email="mail2sridhare@gmail.com",
    license="GNU GPLv3",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.8",
		"Operating System :: OS Independent",
    ],
	py_modules=["mf4-parser"],
    package_dir={'':'src'},
    include_package_data=True,
    install_requires=["asammdf","pandas","numpy","pathlib"],
)