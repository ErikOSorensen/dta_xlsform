from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dta-xlsform",
    version="0.1.0",
    author="Erik Sorensen",
    author_email="erik.sorensen@gmail.com",
    description="Convert Stata .dta files to XLSForm format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ErikOSorensen/dta_xlsform",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pandas>=1.3.0",
        "pyreadstat>=1.1.0",
        "openpyxl>=3.0.0",
    ],
)
