import json
from pathlib import Path

import backtracking as bt

ROOT = Path(__file__).resolve().parent
PASSOS_JSON = ROOT / "passos.json"
CODIGO_FONTE = (ROOT / "backtracking.py").read_text(encoding="utf-8")

# Casa -> [próxima casa] (apenas sentido horário: um único destino por origem)
ADJ = {casa: [] for casa in range(1, 10)}
for origem, destino in bt.PROXIMA_CASA_HORARIO.items():
    ADJ[origem].append(destino)


def cor(peca_indice):
    return "B" if peca_indice < 2 else "P"


def estado_para_letras(estado):
    tabuleiro = {casa: "V" for casa in range(1, 10)}
    for indice, casa in enumerate(estado):
        tabuleiro[casa] = cor(indice)
    return {f"casa{casa}": tabuleiro[casa] for casa in range(1, 10)}


def gerar_passos():
    if not bt.solucao_encontrada:
        raise RuntimeError(
            f"Nenhuma solução encontrada dentro do limite p={bt.profundidade_maxima_permitida} "
            "com a regra apenas horária."
        )

    caminho = bt.pilha_posicoes_do_caminho
    regras = bt.pilha_movimentos_do_caminho
    passos = []

    for indice, estado in enumerate(caminho):
        estado_formatado = estado_para_letras(estado)

        if indice == 0:
            movimento = None
            descricao = (
                "Estado inicial do tabuleiro. Para cada peça, o algoritmo só considera o único "
                "movimento permitido no sentido horário do ciclo (limite de profundidade "
                f"p = {bt.profundidade_maxima_permitida}), evitando revisitar estados do próprio caminho."
            )
            analise = {
                "estadoAnterior": None,
                "casasOcupadas": sorted(estado),
                "movimentosPossiveis": [],
                "movimentoEscolhido": None,
            }
        else:
            estado_anterior = caminho[indice - 1]
            peca_indice = next(i for i in range(4) if estado_anterior[i] != estado[i])
            origem = estado_anterior[peca_indice]
            destino = estado[peca_indice]
            peca = cor(peca_indice)
            casas_ocupadas = sorted(estado_anterior)
            conexoes_disponiveis = ADJ[origem]
            movimentos_possiveis = [casa for casa in conexoes_disponiveis if casa not in estado_anterior]

            movimento = {"peca": peca, "de": origem, "para": destino}

            descricao = (
                f"{regras[indice]}. No estado anterior, as casas ocupadas eram {casas_ocupadas}. "
                "O algoritmo aplicou esse movimento e seguiu a busca a partir desse novo estado."
            )

            analise = {
                "estadoAnterior": estado_para_letras(estado_anterior),
                "casasOcupadas": casas_ocupadas,
                "movimentosPossiveis": movimentos_possiveis,
                "movimentoEscolhido": destino,
                "conexoesAnalisadas": conexoes_disponiveis,
            }

            if indice == len(caminho) - 1:
                descricao += (
                    " Neste ponto, o tabuleiro atingiu a configuração final, então o algoritmo "
                    "encontrou a solução."
                )

        passos.append({
            "indice": indice,
            "estado": estado_formatado,
            "movimento": movimento,
            "descricao": descricao,
            "analise": analise,
            # Conteúdo literal das duas pilhas do algoritmo (backtracking.py),
            # tal como estão em memória logo após este passo ser empilhado.
            "pilhaPosicoesDoCaminho": [list(e) for e in caminho[: indice + 1]],
            "pilhaMovimentosDoCaminho": list(regras[: indice + 1]),
        })

    return passos


def gerar_passos_json():
    passos = gerar_passos()

    return {
        "titulo": "Visualizador de Backtracking do Tabuleiro 3x3",
        "totalPassos": len(passos),
        "solucaoEmMovimentos": len(passos) - 1,
        "voltasBacktrack": bt.total_vezes_que_desfez_jogada,
        "totalImpasses": bt.total_becos_sem_saida,
        "passos": passos,
        "conexoes": {str(origem): destinos for origem, destinos in ADJ.items()},
        "codigoFonte": CODIGO_FONTE,
    }


if __name__ == "__main__":
    dados = gerar_passos_json()

    print(f"Solução encontrada em {dados['solucaoEmMovimentos']} passos!")
    print(f"Total de retrocessos: {dados['voltasBacktrack']} | Total de impasses: {dados['totalImpasses']}\n")
    for passo in dados["passos"]:
        print(f"Passo {passo['indice']}:")
        for linha in ((1, 2, 3), (4, 5, 6), (7, 8, 9)):
            print(" ".join(passo["estado"][f"casa{c}"] for c in linha))
        print("------")

    PASSOS_JSON.write_text(
        json.dumps(dados, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"\npassos.json atualizado em {PASSOS_JSON}")
