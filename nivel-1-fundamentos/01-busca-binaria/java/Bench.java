/**
 * Benchmark: 1.000.000 de consultas em 1.000.000 de elementos (mesmo LCG de bench.py e bench.c).
 * Roda 3 rodadas: a primeira inclui o aquecimento do JIT, as seguintes mostram o regime estável.
 */
public final class Bench {
    private static final int N = 1_000_000;
    private static final int CONSULTAS = 1_000_000;
    private static final int RODADAS = 3;

    public static void main(String[] args) {
        int[] dados = new int[N];
        for (int i = 0; i < N; i++) {
            dados[i] = 2 * i;
        }

        for (int rodada = 1; rodada <= RODADAS; rodada++) {
            long estado = 42;
            long achados = 0;
            long soma = 0;

            long inicio = System.nanoTime();
            for (int q = 0; q < CONSULTAS; q++) {
                estado = estado * 6364136223846793005L + 1442695040888963407L; // wrap-around é definido em Java
                int alvo = (int) ((estado >>> 33) % (2L * N));
                int i = BuscaBinaria.buscar(dados, alvo);
                if (i >= 0) {
                    achados++;
                    soma += i;
                }
            }
            double duracao = (System.nanoTime() - inicio) / 1e9;

            System.out.printf("java    rodada=%d achados=%d soma=%d tempo=%.3fs%n", rodada, achados, soma, duracao);
        }
        System.out.printf("java    memoria do array = %.1f MB%n", (16 + 4L * N) / 1e6);
    }
}
