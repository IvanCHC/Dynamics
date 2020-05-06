from setuptools import setup, find_packages
import dynamics

setup(name='dynamics',
      version=dynamics.__version__,
      url='https://https://github.com/IvanCHC/Dynamics.git',
      author='Ivan Chan',
      author_email='ich.chan26@gmail.com',
      license='GNU General Public License v3.0',
      keywords=['simulation', 'nonlinear dynamics'],
      package=find_packages(),
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.8',
          'Topic :: Scientific/Engineering',
      ],
    )
