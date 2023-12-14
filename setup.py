from setuptools import setup, find_packages

setup(
    name="Stat-386-Package",
    version='0.0.1',
    packages=find_packages(),
    description="A package to aid county-level analysis on cost of living, voting, and other variables",
    author="Michael Miceli & Bryce Martin",
    url="https://github.com/brycemartin52/Stat-386-Project/",
    install_requires = [
        'alabaster',
        'beautifulsoup4',
        'pandas',
        'numpy',
        'uszipcode',
        'urllib3',
        'statsmodels',
        'seaborn',
        'plotly',
        'matplotlib',
        'pkg_resources'
    ],
)

