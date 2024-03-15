
all : clean cluster duplicated static dynamic aggregated multipolicy full
cluster:
	python tests/test_cluster.py
duplicated:
	python tests/test_duplicate_pp.py
static:
	python tests/test_static_weights_pp.py
dynamic:
	python tests/test_dynamic_weights_pp.py
aggregated:
	python tests/test_aggregated_pp.py
multipolicy:
	python tests/test_multi_policy.py
full:
	python tests/test_all_policies.py
real:
	python tests/test_real.py
clean:
	rm -f *.png*
	rm -f *.pkl*
	rm -f test_*.txt
	rm -rf test_*/
deepclean: clean
	rm -rf */*/__pycache__/
	rm -rf __pycache__/
