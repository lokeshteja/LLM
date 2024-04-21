from setuptools import find_packages, setup

setup(
    name='mcqgeneratorapp',
    version='0.0.1',
    author='Lokesh Teja Mamidi',
    install_requires=[
        'openai',
        'langchain',
        'streamlit',
        'python-dotenv',
        'PyPDF2'
    ],
    packages=find_packages()
)
