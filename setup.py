from setuptools import setup, find_packages

setup(
    name='poker_analysis',
    version='0.1',
    packages=find_packages(where='packages'),  # finds game_utils in packages/
    package_dir={'': 'packages'},  # tell setuptools packages are in packages/
    install_requires=[
        'numpy>=1.20',
        'scipy>=1.7',
        'matplotlib>=3.4',
        'sympy>=1.9',
    ],
    python_requires='>=3.8',
    description='Game theory toolkit for poker variant analysis',
    author='Andrew Spears',
)
