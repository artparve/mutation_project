
PYTHON ?= python
PIP ?= $(PYTHON) -m pip

.PHONY: install test mutate mutate_fast htmlcov results clean report mutation_score

install:
	$(PIP) install -r requirements.txt

test:
	PYTHONPATH=. pytest -q

mutate:
	mutmut run

mutate_fast:
	mutmut run --since $(shell git merge-base main HEAD)

htmlcov:
	PYTHONPATH=. pytest --cov=billing --cov-report=html

results:
	mutmut results

report:
	mutmut run --simple-output | tee mutmut.log
	mutmut html

clean:
	rm -rf .mutmut_cache htmlcov .coverage

mutation_score:
	./calculate_mutation_score.sh