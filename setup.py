from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()
setup(
    name="pyfinny",
    version="0.0.1",
    author="Lawrence Lim",
    author_email="ll4715@nyu.edu",
    license="GNU GPLv3",
    description="Financial Statement Analyzer CLI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/larry-lime/pyfinny",
    py_modules=["pyfinny", "app"],
    packages=find_packages(),
    install_requires=[requirements],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    entry_points="""
        [console_scripts]
        cooltool=pyfinny:cli
    """,
)
