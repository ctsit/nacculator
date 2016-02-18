build: egg
egg:
	python setup.py bdist_egg

clean:
	rm -rf dist/ build/ nacculator.egg-info/
	find . -name '*.pyc' | xargs rm
