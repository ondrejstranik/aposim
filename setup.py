import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aposim",
    version="0.0.1",
    author="OndrejStranik",
    author_email="ondra.stranik@gmail.com",
    description="package for apotome structure illumination microscopy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ondrejstranik/aposim",
    packages = setuptools.find_packages(),
    install_requires = [
        'numpy',
        'PyQt5',
        'napari',
        'pytest',
        ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)