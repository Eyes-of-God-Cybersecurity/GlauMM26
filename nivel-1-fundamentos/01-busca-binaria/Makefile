.PHONY: test test-python test-c test-java demo bench clean

test: test-python test-c test-java

test-python:
	cd python && python3 -m unittest

test-c:
	$(MAKE) -C c test

test-java:
	mkdir -p java/out
	javac -Xlint:all -Werror -d java/out java/*.java
	java -cp java/out BuscaBinariaTest

demo:
	cd python && python3 busca_binaria.py
	$(MAKE) -C c demo
	mkdir -p java/out
	javac -Xlint:all -Werror -d java/out java/*.java
	java -cp java/out BuscaBinaria

bench:
	cd python && python3 bench.py
	$(MAKE) -C c bench
	mkdir -p java/out
	javac -d java/out java/*.java
	java -cp java/out Bench

clean:
	$(MAKE) -C c clean
	rm -rf java/out python/__pycache__
