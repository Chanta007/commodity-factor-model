.PHONY: figures check

figures:
	python3 scripts/make_figures.py

check: figures
	python3 tests/check_public.py