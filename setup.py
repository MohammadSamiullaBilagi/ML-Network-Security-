'''
It is essential part of packaging and distributing python projects. Used by setuptools to define configuration of your project such as its metadata, dependencies, and more

'''

from setuptools import find_packages, setup
from typing import List



def get_requirements()->List[str]:
    '''
    This function will return list of requirements
    '''
    requirement_lst:List[str]=[]
    try:
        with open('requirements.txt','r') as file:
            lines=file.readlines()
            for line in lines:
                requirement=line.strip()
                if requirement and requirement !='-e .':
                    requirement_lst.append(requirement)
    
    except FileNotFoundError:
        print("requirements.txt file not found")
    
    return requirement_lst

# setup meta data

setup(
    name="NetworkSecurity",
    version="0.0.0.1",
    author="Sami",
    author_email="mdsamiulla2002@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)