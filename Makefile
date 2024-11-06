
all :pypi clean cluster duplicated static dynamic aggregated multipolicy full
cluster: pypi
	python3.11 examples/test_cluster.py
duplicated: pypi
	python3.11 examples/test_duplicate_pp.py
static:  pypi
	python3.11 examples/test_static_weights_pp.py
dynamic: pypi
	python3.11 examples/test_dynamic_weights_pp.py
kdynamic: pypi
	python3.11 examples/test_k_dynamic_weights_pp.py
aggregated: pypi
	python3.11 examples/test_aggregated_pp.py
multipolicy: pypi
	python3.11 examples/test_multi_policy.py
full: pypi
	python3.11 examples/test_all_policies.py
real: pypi
	python3.11 examples/test_real.py
scale1: pypi
	python3.11 examples/test_scale1.py
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
	pip3.11 install .