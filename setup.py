from setuptools import setup, find_packages

setup(
  name='KarmadaPN',  # Replace with your desired package name
  version='0.1.0',  # Start with version 1.0.0 for initial release
  packages=find_packages(),  # Automatically finds packages
  include_package_data=True,  # Includes data files
  license='GPL',  # Replace with your chosen license
  description=' A Python library for modeling Multi-Cluster Infrastructures based on Karmada using PetriNets ',
  long_description=open('./README.md').read(),  # Reads description from README
  long_description_content_type='text/markdown',  # Sets content type for README
  # Optional arguments
  install_requires=[  # List of dependencies your package needs
      'SNAKES',
      'numpy',
      'networkx',
      

  ],
  
  
  classifiers=[  # Classify your package (optional)
      ],
)

