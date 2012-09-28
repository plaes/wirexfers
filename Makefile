init:
	python setup.py develop
	pip install -r requirements.txt

test:
	nosetests ./tests/*

docs:
	cd docs
	make dirhtml
