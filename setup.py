from setuptools import setup, find_packages

setup(
    name="task-tracker",
    version="1.0.0",
    description="A command-line task management application",
    author="Shukiclaw",
    packages=find_packages(),
    install_requires=[
        "click>=8.0.0",
        "rich>=13.0.0",
    ],
    entry_points={
        "console_scripts": [
            "task-tracker=main:cli",
            "tt=main:cli",
        ],
    },
    python_requires=">=3.8",
)
