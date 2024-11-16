
all :pypi clean cluster duplicated static dynamic aggregated multipolicy full
cluster: pypi
	python examples/test_cluster.py
duplicated: pypi
	python examples/test_duplicate_pp.py
static:  pypi
	python examples/test_static_weights_pp.py
dynamic: pypi
	python examples/test_dynamic_weights_pp.py
kdynamic: pypi
	python examples/test_k_dynamic_weights_pp.py
aggregated: pypi
	python examples/test_aggregated_pp.py
multipolicy: pypi
	python examples/test_multi_policy.py
full: pypi
	python examples/test_all_policies.py
real: pypi
	python examples/test_real.py
scale1: pypi
	python examples/test_scale1.py
clean:
	rm -f *.png*
	rm -f *.pkl*
	rm -f test_*.txt
	rm -rf test_*/
deepclean: clean
	rm -rf */*/__pycache__/
	rm -rf */__pycache__/
	rm -rf __pycache__/
	rm -rf KarmadaPN.egg-info/
	rm -rf build/
pypi:
	pip install .
