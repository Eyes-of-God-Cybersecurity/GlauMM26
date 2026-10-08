import bisect
import random
import unittest

from busca_binaria import (
    busca_binaria,
    busca_binaria_recursiva,
    ip_bloqueado,
    montar_blocklist,
    ponto_medio_ingenuo_32bit,
    ponto_medio_seguro,
)

IMPLEMENTACOES = (busca_binaria, busca_binaria_recursiva)


class TestBuscaBinaria(unittest.TestCase):
    def test_sequencia_vazia(self):
        for f in IMPLEMENTACOES:
            with self.subTest(f=f.__name__):
                self.assertEqual(f([], 1), -1)

    def test_um_elemento(self):
        for f in IMPLEMENTACOES:
            with self.subTest(f=f.__name__):
                self.assertEqual(f([5], 5), 0)
                self.assertEqual(f([5], 4), -1)
                self.assertEqual(f([5], 6), -1)

    def test_exaustivo_ate_64_elementos(self):
        # dados = [0, 2, 4, ...]: todo alvo de -1 a 2n é testado (presentes e ausentes).
        for f in IMPLEMENTACOES:
            for n in range(65):
                dados = [2 * i for i in range(n)]
                for alvo in range(-1, 2 * n + 1):
                    esperado = alvo // 2 if alvo >= 0 and alvo % 2 == 0 and alvo // 2 < n else -1
                    self.assertEqual(f(dados, alvo), esperado, (f.__name__, n, alvo))

    def test_duplicados_devolvem_algum_indice_valido(self):
        dados = [1, 2, 2, 2, 2, 3, 3]
        for f in IMPLEMENTACOES:
            i = f(dados, 2)
            self.assertTrue(1 <= i <= 4)
            self.assertEqual(dados[i], 2)

    def test_negativos_e_inteiros_gigantes(self):
        dados = [-(10**30), -5, 0, 5, 10**30]
        for f in IMPLEMENTACOES:
            self.assertEqual(f(dados, -(10**30)), 0)
            self.assertEqual(f(dados, 10**30), 4)
            self.assertEqual(f(dados, 6), -1)

    def test_aleatorio_contra_bisect(self):
        rng = random.Random(1234)
        for _ in range(500):
            dados = sorted(rng.randint(-50, 50) for _ in range(rng.randint(0, 200)))
            for alvo in range(-60, 61):
                pos = bisect.bisect_left(dados, alvo)
                existe = pos < len(dados) and dados[pos] == alvo
                for f in IMPLEMENTACOES:
                    i = f(dados, alvo)
                    self.assertEqual(i >= 0, existe)
                    if i >= 0:
                        self.assertEqual(dados[i], alvo)

    def test_tipo_incompativel_levanta_erro_em_vez_de_responder_errado(self):
        with self.assertRaises(TypeError):
            busca_binaria([1, 2, 3], "2")


class TestPontoMedio(unittest.TestCase):
    def test_formula_ingenua_estoura_32_bits(self):
        baixo, alto = 1_500_000_000, 2_000_000_000
        self.assertLess(ponto_medio_ingenuo_32bit(baixo, alto), 0)  # fora de [baixo, alto]
        self.assertEqual(ponto_medio_seguro(baixo, alto), 1_750_000_000)

    def test_formulas_coincidem_quando_nao_ha_overflow(self):
        self.assertEqual(ponto_medio_ingenuo_32bit(10, 21), ponto_medio_seguro(10, 21))


class TestBlocklist(unittest.TestCase):
    def setUp(self):
        self.blocklist = montar_blocklist(["203.0.113.7", "198.51.100.23", "192.0.2.10", "192.0.2.10"])

    def test_montagem_ordena_e_remove_duplicatas(self):
        self.assertEqual(len(self.blocklist), 3)
        self.assertEqual(self.blocklist, sorted(self.blocklist))
        self.assertEqual(montar_blocklist(["10.0.0.2", "10.0.0.1"]), [167772161, 167772162])

    def test_consulta(self):
        self.assertTrue(ip_bloqueado(self.blocklist, "198.51.100.23"))
        self.assertTrue(ip_bloqueado(self.blocklist, "192.0.2.10"))
        self.assertFalse(ip_bloqueado(self.blocklist, "198.51.100.24"))
        self.assertFalse(ip_bloqueado([], "192.0.2.10"))

    def test_entrada_invalida_levanta_valueerror(self):
        for ruim in ("", "256.0.0.1", "1.2.3", "abc", "192.0.2.10; DROP", "010.0.0.1"):
            with self.subTest(ip=ruim):
                with self.assertRaises(ValueError):
                    ip_bloqueado(self.blocklist, ruim)


if __name__ == "__main__":
    unittest.main()
