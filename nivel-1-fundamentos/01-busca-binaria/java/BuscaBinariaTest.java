import java.util.Arrays;
import java.util.Random;

/** Testes sem dependências externas (sem JUnit): rode com {@code make test-java}. */
public final class BuscaBinariaTest {
    private static int total = 0;
    private static int falhas = 0;

    private static void verifica(boolean condicao, String descricao) {
        total++;
        if (!condicao) {
            falhas++;
            System.err.println("FALHOU: " + descricao);
        }
    }

    interface Busca {
        int buscar(int[] dados, int alvo);
    }

    private static final Busca[] IMPLEMENTACOES = {BuscaBinaria::buscar, BuscaBinaria::buscarRecursivo};
    private static final String[] NOMES = {"iterativa", "recursiva"};

    static void testeVazia() {
        for (int k = 0; k < IMPLEMENTACOES.length; k++) {
            verifica(IMPLEMENTACOES[k].buscar(new int[0], 1) == -1, NOMES[k] + ": vazia");
        }
    }

    static void testeUmElemento() {
        int[] d = {5};
        for (int k = 0; k < IMPLEMENTACOES.length; k++) {
            verifica(IMPLEMENTACOES[k].buscar(d, 5) == 0, NOMES[k] + ": 1 elemento, achou");
            verifica(IMPLEMENTACOES[k].buscar(d, 4) == -1, NOMES[k] + ": 1 elemento, menor");
            verifica(IMPLEMENTACOES[k].buscar(d, 6) == -1, NOMES[k] + ": 1 elemento, maior");
        }
    }

    static void testeExaustivoAte64() {
        for (int k = 0; k < IMPLEMENTACOES.length; k++) {
            for (int n = 0; n <= 64; n++) {
                int[] d = new int[n];
                for (int i = 0; i < n; i++) {
                    d[i] = 2 * i;
                }
                for (int alvo = -1; alvo <= 2 * n; alvo++) {
                    boolean presente = alvo >= 0 && alvo % 2 == 0 && alvo / 2 < n;
                    int esperado = presente ? alvo / 2 : -1;
                    verifica(IMPLEMENTACOES[k].buscar(d, alvo) == esperado, NOMES[k] + ": n=" + n + " alvo=" + alvo);
                }
            }
        }
    }

    static void testeDuplicados() {
        int[] d = {1, 2, 2, 2, 2, 3, 3};
        for (int k = 0; k < IMPLEMENTACOES.length; k++) {
            int i = IMPLEMENTACOES[k].buscar(d, 2);
            verifica(i >= 1 && i <= 4 && d[i] == 2, NOMES[k] + ": duplicados");
        }
    }

    static void testeExtremosDeInt() {
        int[] d = {Integer.MIN_VALUE, -1, 0, 1, Integer.MAX_VALUE};
        for (int k = 0; k < IMPLEMENTACOES.length; k++) {
            verifica(IMPLEMENTACOES[k].buscar(d, Integer.MIN_VALUE) == 0, NOMES[k] + ": MIN_VALUE");
            verifica(IMPLEMENTACOES[k].buscar(d, Integer.MAX_VALUE) == 4, NOMES[k] + ": MAX_VALUE");
            verifica(IMPLEMENTACOES[k].buscar(d, 2) == -1, NOMES[k] + ": ausente (2)");
            verifica(IMPLEMENTACOES[k].buscar(d, -2) == -1, NOMES[k] + ": ausente (-2)");
        }
    }

    static void testeAleatorioContraArrays() {
        Random rng = new Random(1234);
        for (int rodada = 0; rodada < 500; rodada++) {
            int[] d = new int[rng.nextInt(200)];
            for (int i = 0; i < d.length; i++) {
                d[i] = rng.nextInt(101) - 50;
            }
            Arrays.sort(d);
            for (int alvo = -60; alvo <= 60; alvo++) {
                boolean existe = Arrays.binarySearch(d, alvo) >= 0;
                for (int k = 0; k < IMPLEMENTACOES.length; k++) {
                    int i = IMPLEMENTACOES[k].buscar(d, alvo);
                    verifica((i >= 0) == existe, NOMES[k] + ": aleatorio, existencia");
                    verifica(i < 0 || d[i] == alvo, NOMES[k] + ": aleatorio, indice valido");
                }
            }
        }
    }

    static void testePontoMedio() {
        int baixo = 1_500_000_000;
        int alto = 2_000_000_000;
        verifica(BuscaBinaria.pontoMedioIngenuo(baixo, alto) < 0, "formula ingenua estoura e fica negativa");
        verifica(BuscaBinaria.pontoMedioSeguro(baixo, alto) == 1_750_000_000, "formula segura");
        verifica(BuscaBinaria.pontoMedioSeguro(0, 0) == 0, "ponto medio (0, 0)");
        verifica(BuscaBinaria.pontoMedioSeguro(0, 1) == 0, "ponto medio (0, 1)");
    }

    static void testeNulo() {
        boolean lancou = false;
        try {
            BuscaBinaria.buscar(null, 1);
        } catch (NullPointerException e) {
            lancou = true;
        }
        verifica(lancou, "null levanta NullPointerException");
    }

    public static void main(String[] args) {
        testeVazia();
        testeUmElemento();
        testeExaustivoAte64();
        testeDuplicados();
        testeExtremosDeInt();
        testeAleatorioContraArrays();
        testePontoMedio();
        testeNulo();

        System.out.printf("Java: %d verificacoes, %d falhas%n", total, falhas);
        if (falhas > 0) {
            System.exit(1);
        }
    }
}
