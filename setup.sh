pip install --upgrade pip setuptools wheel
python setup.py sdist bdist_wheel
python3 -m twine check dist/*

python -m twine upload dist/* --username $UNAME -p $PASSWORD --skip-existing
