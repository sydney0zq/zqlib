This package is built for common python usage, and I will update for a long time.

# How to upload to pypi?
# https://juejin.im/post/5d370d94f265da1b8b2b9f71

# 1. Build the package
# pip install --user --upgrade setuptools wheel
python3 setup.py sdist bdist_wheel

# 2. Upload to website
# pip3 install --user --upgrade twine
# python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
python3 -m twine upload dist/*

