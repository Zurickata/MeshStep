from setuptools import setup, find_packages

setup(
    name="quadtree_visualizer",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "PySide6==6.7.0",
        "pyopengl==3.1.7",
        "meshio==5.3.1",
    ],
    # Scripts para ejecutar la aplicación
    entry_points={
        'console_scripts': [
            'quadtree-app=app.main:main',
        ],
    },
)