

test: flake8

flake8:
	flake8 upbrew.py setup.py

clean:
	rm -rf build
	rm -rf dist

app:
	python setup.py py2app
