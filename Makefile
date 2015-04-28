

test: flake8

flake8:
	flake8 upbrew.py setup.py

setup:
	virtualenv env
	env/bin/pip install -r requirements.txt

clean:
	rm -rf build
	rm -rf dist

app:
	python setup.py py2app

pkg:
	python setup.py bdist_mpkg
