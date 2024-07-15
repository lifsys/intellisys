from setuptools import setup, find_packages

# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="intellisys",
    version="0.1.1",
    author="Lifsys Enterprise",
    author_email="contact@lifsys.com",
    description="Intelligence/AI services for the Lifsys Enterprise",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lifsys/intellisys",
    packages=find_packages(exclude=["tests*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "openai>=1.0.0",
        "litellm>=1.0.0",
        "jinja2>=3.0.0",
        "onepasswordconnectsdk>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "flake8>=3.9",
            "black>=21.5b1",
        ],
    },
    project_urls={
        "Bug Tracker": "https://github.com/lifsys/intellisys/issues",
        "Documentation": "https://intellisys.readthedocs.io/",
        "Source Code": "https://github.com/lifsys/intellisys",
    },
)
