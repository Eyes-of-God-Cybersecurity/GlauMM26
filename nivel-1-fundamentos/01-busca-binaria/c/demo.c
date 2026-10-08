#include <inttypes.h>
#include <stdio.h>

#include "busca_binaria.h"

int main(void)
{
    const int dados[] = {2, 3, 5, 7, 11, 13, 17, 19, 23};
    const size_t n = sizeof dados / sizeof dados[0];
    const int alvos[] = {7, 23, 2, 4, 30};

    for (size_t k = 0; k < sizeof alvos / sizeof alvos[0]; k++)
        printf("busca_binaria(dados, %zu, %d) -> %td\n", n, alvos[k], busca_binaria(dados, n, alvos[k]));

    /*
     * Bug do ponto médio. Com int com sinal, (baixo + alto) estourando é comportamento
     * indefinido; usamos uint32_t, cujo wrap-around é definido, para a demo ser determinística.
     */
    uint32_t baixo = 3000000000u;
    uint32_t alto = 4000000000u;
    uint32_t ingenuo = (baixo + alto) / 2;
    uint32_t seguro = baixo + (alto - baixo) / 2;

    printf("ponto medio ingenuo (%" PRIu32 ", %" PRIu32 ") -> %" PRIu32 "  (fora do intervalo!)\n", baixo, alto, ingenuo);
    printf("ponto medio seguro  (%" PRIu32 ", %" PRIu32 ") -> %" PRIu32 "\n", baixo, alto, seguro);
    return 0;
}
