.PHONY: figures check test demo build

figures:
	python3 scripts/make_figures.py

check: figures
	python3 tests/check_public.py

test:
	python3 -m unittest discover -s tests -p "test_*.py" -v

demo:
	python3 scripts/estimate.py --demo

build: check test demo