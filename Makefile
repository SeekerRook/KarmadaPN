
all : clean cluster duplicated static dynamic aggregated multipolicy full
cluster:
	python test_cluster.py
duplicated:
	python test_duplicate_pp.py
static:
	python test_static_weights_pp.py
dynamic:
	python test_dynamic_weights_pp.py
aggregated:
	python test_aggregated_pp.py
multipolicy:
	python test_multi_policy.py
full:
	python test_all_policies.py
clean:
	rm -f *.png*
	rm -f *.pkl*
	rm -f test_*.txt
	rm -rf test_*/
deepclean: clean
	rm -rf */*/__pycache__/
	rm -rf __pycache__/
