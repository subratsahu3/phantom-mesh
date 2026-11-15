from setuptools import setup, find_packages

setup(
    name="phantom-mesh",
    version="1.0.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "phantom-mesh = phantom_mesh.cli:main",
        ],
    },
    python_requires=">=3.9",
)
