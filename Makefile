
all :pypi clean cluster duplicated static dynamic aggregated multipolicy full
cluster:
	python examples/test_cluster.py
duplicated:
	python examples/test_duplicate_pp.py
static:
	python examples/test_static_weights_pp.py
dynamic:
	python examples/test_dynamic_weights_pp.py
aggregated:
	python examples/test_aggregated_pp.py
multipolicy:
	python examples/test_multi_policy.py
full:
	python examples/test_all_policies.py
real:
	python examples/test_real.py
clean:
	rm -f *.png*
	rm -f *.pkl*
	rm -f test_*.txt
	rm -rf test_*/
deepclean: clean
	rm -rf */*/__pycache__/
	rm -rf __pycache__/
pypi:
	pip install .