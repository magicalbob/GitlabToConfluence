pip install -r requirements.txt
~/.local/bin/coverage run -m unittest discover -v -s ./ -p '*_unittest.py'
~/.local/bin/coverage xml
rm -rf __pycache__
