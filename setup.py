from setuptools import setup

setup(name='dynamics',
      version='0.0.1',
      url='https://https://github.com/IvanCHC/Dynamics.git',
      author='Chon-Hou Ivan Chan',
      author_email='ich.chan26@gmail.com',
      license='LICENSE',
      keywords='simulation',
      package =[
          '.',
          'dynamics',
      ],
      install_requires=[
          'numpy',
          'scipy',
          'matplotlib',
          'pyqt5',
          'pyqtgraph'      
      ],
    )
