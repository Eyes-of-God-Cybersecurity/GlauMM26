import java.util.Objects;

/**
 * Busca binária — Nível 1 (Fundamentos), módulo 01.
 *
 * <p>Mesmas convenções das versões em Python e C: intervalo semiaberto [baixo, alto),
 * devolve um índice com {@code dados[i] == alvo} ou -1, e exige a sequência ordenada.
 */
public final class BuscaBinaria {
    private BuscaBinaria() {}

    /** Versão iterativa. Tempo O(log n), espaço O(1). */
    public static int buscar(int[] dados, int alvo) {
        Objects.requireNonNull(dados, "dados");
        int baixo = 0;
        int alto = dados.length;
        while (baixo < alto) {
            int meio = pontoMedioSeguro(baixo, alto);
            if (dados[meio] == alvo) {
                return meio;
            }
            if (dados[meio] < alvo) {
                baixo = meio + 1;
            } else {
                alto = meio;
            }
        }
        return -1;
    }

    /** Versão recursiva. Profundidade máxima ~log2(n). */
    public static int buscarRecursivo(int[] dados, int alvo) {
        Objects.requireNonNull(dados, "dados");
        return buscarRecursivo(dados, alvo, 0, dados.length);
    }

    private static int buscarRecursivo(int[] dados, int alvo, int baixo, int alto) {
        if (baixo >= alto) {
            return -1;
        }
        int meio = pontoMedioSeguro(baixo, alto);
        if (dados[meio] == alvo) {
            return meio;
        }
        if (dados[meio] < alvo) {
            return buscarRecursivo(dados, alvo, meio + 1, alto);
        }
        return buscarRecursivo(dados, alvo, baixo, meio);
    }

    /** O bug de 2006: em int de 32 bits, baixo + alto passa de 2^31 - 1 e vira negativo. */
    static int pontoMedioIngenuo(int baixo, int alto) {
        return (baixo + alto) / 2;
    }

    static int pontoMedioSeguro(int baixo, int alto) {
        return baixo + (alto - baixo) / 2;
    }

    public static void main(String[] args) {
        int[] dados = {2, 3, 5, 7, 11, 13, 17, 19, 23};
        for (int alvo : new int[] {7, 23, 2, 4, 30}) {
            System.out.printf("buscar(%s, %d) -> %d%n", java.util.Arrays.toString(dados), alvo, buscar(dados, alvo));
        }

        int baixo = 1_500_000_000;
        int alto = 2_000_000_000;
        System.out.printf("ponto medio ingenuo (%d, %d) -> %d%n", baixo, alto, pontoMedioIngenuo(baixo, alto));
        System.out.printf("ponto medio seguro  (%d, %d) -> %d%n", baixo, alto, pontoMedioSeguro(baixo, alto));
    }
}
