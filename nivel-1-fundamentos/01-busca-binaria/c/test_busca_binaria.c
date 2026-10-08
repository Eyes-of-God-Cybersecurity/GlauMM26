#include <limits.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#include "busca_binaria.h"

static int total = 0;
static int falhas = 0;

/* Macro própria: assert() some quando compilado com -DNDEBUG. */
#define VERIFICA(cond)                                                        \
    do {                                                                      \
        total++;                                                              \
        if (!(cond)) {                                                        \
            falhas++;                                                         \
            fprintf(stderr, "FALHOU %s:%d: %s\n", __FILE__, __LINE__, #cond); \
        }                                                                     \
    } while (0)

static ptrdiff_t busca_linear(const int *d, size_t n, int alvo)
{
    for (size_t i = 0; i < n; i++)
        if (d[i] == alvo)
            return (ptrdiff_t)i;
    return -1;
}

static int compara_int(const void *a, const void *b)
{
    int x = *(const int *)a;
    int y = *(const int *)b;
    return (x > y) - (x < y);
}

static void teste_vazia(void)
{
    const int x[1] = {0};
    VERIFICA(busca_binaria(NULL, 0, 1) == -1);
    VERIFICA(busca_binaria(x, 0, 0) == -1); /* n == 0: x[0] nunca pode ser lido */
}

static void teste_um_elemento(void)
{
    const int d[] = {5};
    VERIFICA(busca_binaria(d, 1, 5) == 0);
    VERIFICA(busca_binaria(d, 1, 4) == -1);
    VERIFICA(busca_binaria(d, 1, 6) == -1);
}

static void teste_exaustivo_ate_64(void)
{
    int d[64];
    for (size_t n = 0; n <= 64; n++) {
        for (size_t i = 0; i < n; i++)
            d[i] = (int)(2 * i);
        for (int alvo = -1; alvo <= (int)(2 * n); alvo++) {
            int presente = alvo >= 0 && alvo % 2 == 0 && (size_t)(alvo / 2) < n;
            ptrdiff_t esperado = presente ? alvo / 2 : -1;
            VERIFICA(busca_binaria(d, n, alvo) == esperado);
        }
    }
}

static void teste_duplicados(void)
{
    const int d[] = {1, 2, 2, 2, 2, 3, 3};
    ptrdiff_t i = busca_binaria(d, 7, 2);
    VERIFICA(i >= 1 && i <= 4);
    VERIFICA(i >= 0 && d[i] == 2);
}

static void teste_extremos_de_int(void)
{
    const int d[] = {INT_MIN, -1, 0, 1, INT_MAX};
    VERIFICA(busca_binaria(d, 5, INT_MIN) == 0);
    VERIFICA(busca_binaria(d, 5, INT_MAX) == 4);
    VERIFICA(busca_binaria(d, 5, 2) == -1);
    VERIFICA(busca_binaria(d, 5, -2) == -1);
}

static void teste_aleatorio_contra_busca_linear(void)
{
    int d[200];
    srand(1234);
    for (int rodada = 0; rodada < 500; rodada++) {
        size_t n = (size_t)(rand() % 200);
        for (size_t i = 0; i < n; i++)
            d[i] = rand() % 101 - 50;
        qsort(d, n, sizeof d[0], compara_int);
        for (int alvo = -60; alvo <= 60; alvo++) {
            ptrdiff_t i = busca_binaria(d, n, alvo);
            VERIFICA((i >= 0) == (busca_linear(d, n, alvo) >= 0));
            VERIFICA(i < 0 || d[i] == alvo);
        }
    }
}

static void teste_ponto_medio(void)
{
    VERIFICA(ponto_medio(0, 0) == 0);
    VERIFICA(ponto_medio(0, 1) == 0);
    VERIFICA(ponto_medio(0, 2) == 1);
    VERIFICA(ponto_medio(SIZE_MAX - 10, SIZE_MAX) == SIZE_MAX - 5); /* (baixo+alto)/2 estouraria */
}

int main(void)
{
    teste_vazia();
    teste_um_elemento();
    teste_exaustivo_ate_64();
    teste_duplicados();
    teste_extremos_de_int();
    teste_aleatorio_contra_busca_linear();
    teste_ponto_medio();

    printf("C: %d verificacoes, %d falhas\n", total, falhas);
    return falhas ? 1 : 0;
}
