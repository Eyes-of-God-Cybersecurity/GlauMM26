"""Benchmark: 1.000.000 de consultas em 1.000.000 de elementos.

As três linguagens usam o mesmo gerador congruencial linear (LCG), então o checksum
(achados e soma dos índices) deve ser idêntico nas três.
"""
import sys
import time

from busca_binaria import busca_binaria

N = 1_000_000
CONSULTAS = 1_000_000
MASCARA_64 = (1 << 64) - 1


def main() -> None:
    dados = [2 * i for i in range(N)]
    estado, achados, soma = 42, 0, 0

    inicio = time.perf_counter()
    for _ in range(CONSULTAS):
        estado = (estado * 6364136223846793005 + 1442695040888963407) & MASCARA_64
        i = busca_binaria(dados, (estado >> 33) % (2 * N))
        if i >= 0:
            achados += 1
            soma += i
    duracao = time.perf_counter() - inicio

    memoria = sys.getsizeof(dados) + sum(sys.getsizeof(x) for x in dados)
    print(f"python  achados={achados} soma={soma} tempo={duracao:.3f}s")
    print(f"python  memória do array ≈ {memoria / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
