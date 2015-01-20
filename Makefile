

clean:
	rm -rf build
	rm -rf dist

app:
	python setup.py py2app
