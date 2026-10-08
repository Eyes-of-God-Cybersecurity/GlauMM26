#include "busca_binaria.h"

size_t ponto_medio(size_t baixo, size_t alto)
{
    /* (baixo + alto) / 2 pode estourar; alto - baixo nunca estoura se baixo <= alto. */
    return baixo + (alto - baixo) / 2;
}

ptrdiff_t busca_binaria(const int *dados, size_t n, int alvo)
{
    /*
     * Intervalo semiaberto [baixo, alto). Com size_t (sem sinal), a forma fechada
     * "alto = meio - 1" daria a volta (wrap-around) para SIZE_MAX quando meio == 0.
     */
    size_t baixo = 0;
    size_t alto = n;

    while (baixo < alto) {
        size_t meio = ponto_medio(baixo, alto);

        if (dados[meio] == alvo)
            return (ptrdiff_t)meio;
        if (dados[meio] < alvo)
            baixo = meio + 1;
        else
            alto = meio;
    }
    return -1;
}
