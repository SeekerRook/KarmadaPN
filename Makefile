
all : cluster duplicated
cluster:
	python test_cluster.py

duplicated:
	python test_duplicate_pp.py

clean:
	rm *.png*
	rm test_*.txt