from setuptools import find_packages, setup

setup(
    name="rater-pandas",
    version="0.0.10",
    description="A Python library that simplifies the calculation of interrater and intrarater reliability metrics directly from pandas DataFrames.",
    packages=find_packages(),  # Automatically find packages in the current directory
    url="https://github.com/Confusion1224/rater-pandas",
    author="Confusion1224",
    author_email="chkoad@connect.ust.hk",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.6',
    install_requires=[
        "pandas>=1.0.0",
        "numpy>=1.18.0",
        "statsmodels>=0.13.0",
        "krippendorff>=0.8.1",
        "pingouin>=0.5.5",
        "scipy>=1.15.3"
    ],
)