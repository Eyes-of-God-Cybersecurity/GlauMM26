/* Benchmark: 1.000.000 de consultas em 1.000.000 de elementos (mesmo LCG de bench.py e Bench.java). */
#define _POSIX_C_SOURCE 199309L

#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "busca_binaria.h"

#define N 1000000u
#define CONSULTAS 1000000u

int main(void)
{
    int *dados = malloc(N * sizeof *dados);
    if (dados == NULL) {
        perror("malloc");
        return 1;
    }
    for (size_t i = 0; i < N; i++)
        dados[i] = (int)(2 * i);

    uint64_t estado = 42, achados = 0, soma = 0;
    struct timespec t0, t1;

    clock_gettime(CLOCK_MONOTONIC, &t0);
    for (uint32_t q = 0; q < CONSULTAS; q++) {
        estado = estado * 6364136223846793005ULL + 1442695040888963407ULL;
        int alvo = (int)((estado >> 33) % (2ULL * N));
        ptrdiff_t i = busca_binaria(dados, N, alvo);
        if (i >= 0) {
            achados++;
            soma += (uint64_t)i;
        }
    }
    clock_gettime(CLOCK_MONOTONIC, &t1);

    double duracao = (double)(t1.tv_sec - t0.tv_sec) + (double)(t1.tv_nsec - t0.tv_nsec) / 1e9;
    printf("c       achados=%" PRIu64 " soma=%" PRIu64 " tempo=%.3fs\n", achados, soma, duracao);
    printf("c       memoria do array = %.1f MB\n", (double)(N * sizeof *dados) / 1e6);

    free(dados);
    return 0;
}
