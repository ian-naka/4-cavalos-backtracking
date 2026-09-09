# ==============================================================================
# MODELAGEM DO PROBLEMA DOS 4 CAVALOS - RESTRIÇÃO: APENAS SENTIDO HORÁRIO
# ==============================================================================

# Grafo de transição com movimento ÚNICO por casa (Apenas Sentido Horário)
CONEXAO_HORARIA = {
    1: 6, 6: 7, 7: 2, 2: 9,
    9: 4, 4: 3, 3: 8, 8: 1
}

PECAS = ["Branco 1 (B1)", "Branco 2 (B2)", "Preto 1 (P1)", "Preto 2 (P2)"]

# Estado Inicial: [B1, B2, P1, P2]
estado_inicial = [1, 3, 7, 9]

# Pilhas para a solução efetiva
caminho_estados = [estado_inicial]
caminho_regras = ["Estado Inicial"]

# Contadores de execução
total_impasses = 0
total_retrocessos = 0


def eh_objetivo(estado):
    """TESTE DE OBJETIVO: Brancos em {7, 9} e Pretos em {1, 3}"""
    brancos = {estado[0], estado[1]}
    pretos  = {estado[2], estado[3]}
    return brancos == {7, 9} and pretos == {1, 3}


def busca_backtracking(estado_atual, limite_p=20):
    global total_impasses, total_retrocessos

    # 1. TESTE DE OBJETIVO
    if eh_objetivo(estado_atual):
        return True

    # 2. IMPASSE POR PROFUNDIDADE (Limite p)
    if len(caminho_estados) >= limite_p:
        total_impasses += 1
        return False

    # 3. GERAÇÃO DE REGRAS (Apenas a próxima casa no sentido horário)
    for i in range(4):
        pos_atual = estado_atual[i]
        prox_pos = CONEXAO_HORARIA[pos_atual]  # Destino único determinado pelo sentido horário

        # Condição 1: Casa de destino VAZIA
        if prox_pos not in estado_atual:
            novo_estado = list(estado_atual)
            novo_estado[i] = prox_pos

            # Condição 2: CORTE DE CICLOS (evita repetição no caminho)
            if novo_estado not in caminho_estados:
                regra_aplicada = f"Mover {PECAS[i]} da casa {pos_atual} para a casa {prox_pos} (Horário)"

                # --- AVANÇO ---
                caminho_estados.append(novo_estado)
                caminho_regras.append(regra_aplicada)

                # Chamada Recursiva
                if busca_backtracking(novo_estado, limite_p):
                    return True

                # --- RETROCESSO (BACKTRACKING EM IMPASSE) ---
                caminho_estados.pop()
                caminho_regras.pop()
                total_impasses += 1
                total_retrocessos += 1

    # 4. IMPASSE NATURAL (Sem jogadas válidas no nó atual)
    return False


# ==============================================================================
# EXECUÇÃO E IMPRESSÃO DO RESUMO FINAL
# ==============================================================================
limite_profundidade = 17
sucesso = busca_backtracking(estado_inicial, limite_p=limite_profundidade)

if __name__ == "__main__":
    if sucesso:
        print("=" * 80)
        print(" RESUMO DA EXECUÇÃO - BACKTRACKING (REGRA RESTRITA: SENTIDO HORÁRIO)")
        print("=" * 80)
        print(f" Total de impasses/erros encontrados : {total_impasses}")
        print(f" Total de retrocessos (pop) realizados: {total_retrocessos}")
        print(f" TOTAL DE PASSOS DA MELHOR SOLUÇÃO   : {len(caminho_estados) - 1}")
        print("=" * 80 + "\n")

        print("CAMINHO FINAL DA SOLUÇÃO (PASSOS EFETIVOS LIMPOS):")
        print("-" * 80)
        for passo in range(len(caminho_estados)):
            est = caminho_estados[passo]
            regra = caminho_regras[passo]
            if passo == 0:
                print(f"Passo {passo:02d} [INÍCIO]: {regra}")
            else:
                print(f"Passo {passo:02d} [REGRA] : {regra}")
            print(f"         [ESTADO]: B1 na casa {est[0]} | B2 na casa {est[1]} | P1 na casa {est[2]} | P2 na casa {est[3]}")
            print("-" * 80)
    else:
        print(f"\nNenhuma solução encontrada dentro do limite p={limite_profundidade} com a regra apenas horária.")
