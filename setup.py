import setuptools


with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

setuptools.setup(
    name="myresume",
    version="0.0.1",
    author="Albert Hopkins",
    author_email="marduk@letterboxes.org",
    description="Create resumes from YAML description files",
    long_description=long_description,
    url="https://github.com/enku/myresume",
    license="GPLv3",
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.6",
    install_requires=["Jinja2>=2.11.2,<3.0", "PyYAML>=5.3.1,<6.0",],
    entry_points={
        "console_scripts": ["myresume = myresume.cli:main"],
        "myresume.themes": ["default = myresume.themes.default",],
    },
)
