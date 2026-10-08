"""Busca binária — Nível 1 (Fundamentos), módulo 01.

O mesmo algoritmo existe em C (../c) e Java (../java). Convenções comuns às três:
  * intervalo semiaberto [baixo, alto): o alvo, se existir, está em dados[baixo:alto]
  * devolve um índice i com dados[i] == alvo, ou -1
  * pré-condição: a sequência está ordenada de forma não decrescente
"""
from __future__ import annotations

import ipaddress
from collections.abc import Iterable, Sequence


def busca_binaria(dados: Sequence[int], alvo: int) -> int:
    """Versão iterativa. Tempo O(log n), espaço O(1)."""
    baixo, alto = 0, len(dados)
    while baixo < alto:
        # Em Python o inteiro não estoura, mas mantemos a forma segura das outras linguagens.
        meio = baixo + (alto - baixo) // 2
        if dados[meio] == alvo:
            return meio
        if dados[meio] < alvo:
            baixo = meio + 1
        else:
            alto = meio
    return -1


def busca_binaria_recursiva(
    dados: Sequence[int], alvo: int, baixo: int = 0, alto: int | None = None
) -> int:
    """Versão recursiva. Profundidade máxima ~log2(n): não há risco de estourar a pilha."""
    if alto is None:
        alto = len(dados)
    if baixo >= alto:
        return -1
    meio = baixo + (alto - baixo) // 2
    if dados[meio] == alvo:
        return meio
    if dados[meio] < alvo:
        return busca_binaria_recursiva(dados, alvo, meio + 1, alto)
    return busca_binaria_recursiva(dados, alvo, baixo, meio)


# --- Segurança: o bug do ponto médio --------------------------------------------------------

def _como_int32(x: int) -> int:
    """Simula o wrap-around de um int de 32 bits com sinal (o que Java faz)."""
    return (x + 2**31) % 2**32 - 2**31


def ponto_medio_ingenuo_32bit(baixo: int, alto: int) -> int:
    """(baixo + alto) / 2 como ficaria num int de 32 bits. Estoura para índices grandes."""
    return int(_como_int32(baixo + alto) / 2)  # divisão de Java trunca em direção a zero


def ponto_medio_seguro(baixo: int, alto: int) -> int:
    return baixo + (alto - baixo) // 2


# --- Aplicação em Cybersecurity: consulta a uma blocklist de IPs ------------------------------

def montar_blocklist(ips: Iterable[str]) -> list[int]:
    """Converte IPv4 em inteiros, remove duplicatas e ordena.

    Ordenar na carga garante a pré-condição da busca: com uma lista fora de ordem a busca
    não falha de forma visível, ela apenas responde "não bloqueado" para IPs que deveriam
    ser bloqueados (falha aberta).
    """
    return sorted({int(ipaddress.IPv4Address(ip)) for ip in ips})


def ip_bloqueado(blocklist: Sequence[int], ip: str) -> bool:
    """Levanta ValueError para entrada inválida: quem chama decide o que fazer.

    ipaddress rejeita zeros à esquerda ("010.0.0.1"); parsers em C (inet_aton) leem isso
    como octal. Divergência entre parsers é uma fonte clássica de bypass de blocklist/SSRF.
    """
    return busca_binaria(blocklist, int(ipaddress.IPv4Address(ip))) != -1


def _demo() -> None:
    dados = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    for alvo in (7, 23, 2, 4, 30):
        print(f"busca_binaria({dados}, {alvo}) -> {busca_binaria(dados, alvo)}")

    baixo, alto = 1_500_000_000, 2_000_000_000
    print(f"ponto médio ingênuo ({baixo}, {alto}) -> {ponto_medio_ingenuo_32bit(baixo, alto)}")
    print(f"ponto médio seguro  ({baixo}, {alto}) -> {ponto_medio_seguro(baixo, alto)}")

    # Endereços reservados para documentação (RFC 5737).
    blocklist = montar_blocklist(["203.0.113.7", "198.51.100.23", "192.0.2.10"])
    for ip in ("198.51.100.23", "198.51.100.24"):
        print(f"ip_bloqueado({ip}) -> {ip_bloqueado(blocklist, ip)}")


if __name__ == "__main__":
    _demo()
