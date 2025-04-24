from setuptools import setup, find_packages

setup(
    name="dunkelflaute",
    version="0.1.0",
    author="Philipp Härtel",
    author_email="philipp.haertel@iee.fraunhofer.de",
    description="A module for analyzing and visualizing periods of low renewable energy production.",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "matplotlib",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
