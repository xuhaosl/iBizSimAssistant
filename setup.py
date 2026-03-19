from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="iBizSimAssistant",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A web automation assistant for data extraction and Excel integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/iBizSimAssistant",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "playwright>=1.40.0",
        "openpyxl>=3.1.2",
        "pyyaml>=6.0.1",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-asyncio>=0.21.1",
        ],
    },
    entry_points={
        "console_scripts": [
            "ibizsim=src.main:main",
        ],
    },
)
