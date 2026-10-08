#ifndef BUSCA_BINARIA_H
#define BUSCA_BINARIA_H

#include <stddef.h>

/*
 * Devolve um índice i com dados[i] == alvo, ou -1 se o alvo não existir.
 *
 * Pré-condições (violá-las é comportamento indefinido, o C não verifica nada):
 *   - dados aponta para n ints válidos, ordenados de forma não decrescente
 *     (com n == 0, dados pode ser NULL);
 *   - n não passa de PTRDIFF_MAX, o que vale para qualquer objeto real.
 *
 * Ao contrário de Python e Java, o array não carrega o próprio tamanho:
 * quem chama é responsável por passar o n correto.
 */
ptrdiff_t busca_binaria(const int *dados, size_t n, int alvo);

/* Ponto médio sem overflow, para baixo <= alto. */
size_t ponto_medio(size_t baixo, size_t alto);

#endif
