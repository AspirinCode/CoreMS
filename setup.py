import pathlib

import setuptools
from setuptools import find_packages, setup



# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()
# This call to setup() does all the work
setup(
    name="enviroms",
    version="0.1.0",
    description="Object Oriented Mass Spectrometry ToolBox",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://gitlab.pnnl.gov/corilo/enviroms/",
    author="Corilo, Yuri",
    author_email="corilo@pnnl.gov",
    license="Not decided yet",
    classifiers=[
        #"License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages= setuptools.find_packages(".", exclude= ["*.test", "*.win_only", "libs", "bokeh_imple"]),
    exclude_package_data={'.': ['./enviroms/emsl/yec/input/win_only/ThermoRaw.py']},
    include_package_data=True,
    install_requires=["pandas", "numpy", "matplotlib"],
    #entry_points={
    #    "console_scripts": [
    #        "realpython=reader.__main__:main",

    #    ]
    #},
)
