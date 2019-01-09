build: egg
egg:
	python setup.py bdist_egg

tests: ALWAYS
	PTYHONPATH=. python -m unittest discover tests "*_test.py"

clean: ALWAYS
	rm -rf dist/ build/ nacculator.egg-info/
	find . -name '*.pyc' | xargs rm

ALWAYS:
