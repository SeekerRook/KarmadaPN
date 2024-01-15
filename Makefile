
all : cluster duplicated static
cluster:
	python test_cluster.py

duplicated:
	python test_duplicate_pp.py


static:
	python test_static_weights_pp.py

clean:
	rm *.png*
	rm test_*.txt