from setuptools import setup, find_packages

setup(
    name="emloan",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy", "pandas", "plotly"
    ],
    author="Emanuel Pegler",
    author_email="manuel.pegler@gmail.com",
    description="A description of your project",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12',
)