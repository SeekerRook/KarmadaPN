
all : cluster duplicated static dynamic
cluster:
	python test_cluster.py

duplicated:
	python test_duplicate_pp.py


static:
	python test_static_weights_pp.py


dynamic:
	python test_dynamic_weights_pp.py

clean:
	rm *.png*
	rm test_*.txt
	rm -r test_*/