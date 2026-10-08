CC      ?= gcc
CFLAGS  := -std=c11 -Wall -Wextra -Wpedantic -Werror
# Testes rodam com AddressSanitizer + UBSan: leituras fora do array e overflow com sinal viram erro.
SANITIZE := -O1 -g -fsanitize=address,undefined -fno-sanitize-recover=all -fno-omit-frame-pointer

.PHONY: demo test bench clean

demo: build/demo
	./build/demo

test: build/test_busca_binaria
	./build/test_busca_binaria

bench: build/bench
	./build/bench

build/demo: demo.c busca_binaria.c busca_binaria.h | build
	$(CC) $(CFLAGS) -O2 -o $@ demo.c busca_binaria.c

build/test_busca_binaria: test_busca_binaria.c busca_binaria.c busca_binaria.h | build
	$(CC) $(CFLAGS) $(SANITIZE) -o $@ test_busca_binaria.c busca_binaria.c

build/bench: bench.c busca_binaria.c busca_binaria.h | build
	$(CC) $(CFLAGS) -O2 -o $@ bench.c busca_binaria.c

build:
	mkdir -p build

clean:
	rm -rf build
