
from setuptools import setup, find_packages

setup(
    name='zqlib',
    version='0.1.8',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='Common used package of Qiang Zhou',
    long_description=open('README.txt').read(),
    install_requires=['numpy', 'opencv-python'],
    url='https://github.com/BillMills/python-package-example',
    author='Qiang Zhou',
    author_email='theodoruszq@gmail.com'
)
