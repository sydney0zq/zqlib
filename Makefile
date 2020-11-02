#
# Makefile
# qiang.zhou, 2020-01-10 16:24
#

clean:
	@echo "Makefile needs your attention"
	/bin/rm -rf dist/*

release:
	/bin/rm -rf dist/* build/
	python3 setup.py sdist bdist_wheel
	python3 -m twine upload dist/*



# vim:ft=make
#
