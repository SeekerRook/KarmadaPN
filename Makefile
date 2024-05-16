
all :pypi clean cluster duplicated static dynamic aggregated multipolicy full
cluster:
	python3.11 examples/test_cluster.py
duplicated:
	python3.11 examples/test_duplicate_pp.py
static:
	python3.11 examples/test_static_weights_pp.py
dynamic:
	python3.11 examples/test_dynamic_weights_pp.py
aggregated:
	python3.11 examples/test_aggregated_pp.py
multipolicy:
	python3.11 examples/test_multi_policy.py
full:
	python3.11 examples/test_all_policies.py
real:
	python3.11 examples/test_real.py
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