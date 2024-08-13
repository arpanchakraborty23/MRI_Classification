from setuptools import setup,find_packages
from typing import List

HYPEN_E_DOT='-e .'

def get_requirements(file_path:str)->[list]:
    requirements=[]
    with open(file_path,'r') as f:
        requirements=f.readlines()
        requirements=[req.replace('/n',' ') for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)

    return requirements

setup(
    name='MRI-CLASSIFICATION',
    version='0.1',
    author='Arpan Chakraborty',
    author_email='ArpanchakrabortyDS@gmail.com',
    url='https://github.com/arpanchakraborty23/MRI_Classification.git',
    packages=find_packages(),
    install_requries=get_requirements('requirements.txt')
)