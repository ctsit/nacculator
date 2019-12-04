build: egg
egg:
	python setup.py bdist_egg

tests: ALWAYS
	python -m unittest

clean: ALWAYS
	rm -rf dist/ build/ nacculator.egg-info/
	find . -name '*.pyc' | xargs rm

ALWAYS:
