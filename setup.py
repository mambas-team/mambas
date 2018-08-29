from setuptools import setup
from setuptools import find_packages

setup(name="mambas",
      version="0.1",
      description="Web based visualization tool to monitor your Keras training",
      author="Kevin Beck",
      author_email="misterkevinski@gmail.com",
      url="https://github.com/misterkevinski/mambas",
      license="MIT",
      include_package_data=True,
      install_requires=["bottle", "keras"],
      packages=find_packages())