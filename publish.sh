pip install --upgrade setuptools wheel tqdm
pip install twine
rm -rf build/ dist/ *.egg-info
python setup.py sdist bdist_wheel
twine upload dist/*
