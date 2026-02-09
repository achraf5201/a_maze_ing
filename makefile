all:run

build: clean
	python3 setup.py sdist bdist_wheel
	cp dist/*.tar.gz .
	cp dist/*.whl .
	@echo "Package created in root directory."

debug:
	python3 -m pdb a_maze_ing.py 

install: build
	pip install  mazegen-1.0.0.tar.gz --force-reinstall
	pip install mazegen-1.0.0-py3-none-any.whl --force-reinstall

run:
	python3 a_maze_ing.py $(ARGS)

clean:
	rm -rf build/ dist/ mazegen/__pycache__ *.egg-info __pycache__ .mypy_cache \
	rm -rf *output*.txt
	rm -rf src/__pycache__ src/*.egg-info
	rm -rf *.whl *.tar.gz 

lint:
	python3 -m flake8 .
	python3 -m mypy . \
	--warn-return-any \
	--warn-unused-ignores \
	--ignore-missing-imports \
	--disallow-untyped-defs \
	--check-untyped-defs
