# ==============================================================================
# MODELAGEM DO PROBLEMA DOS 4 CAVALOS - RESTRIÇÃO: APENAS SENTIDO HORÁRIO
# (versão com nomenclatura revisada para maior clareza)
# ==============================================================================
 
# Grafo de transição com movimento ÚNICO por casa (Apenas Sentido Horário)
# Mapeia: casa atual -> única casa de destino permitida
PROXIMA_CASA_HORARIO = {
    1: 6, 6: 7, 7: 2, 2: 9,
    9: 4, 4: 3, 3: 8, 8: 1
}
 
NOMES_PECAS = ["Branco 1 (B1)", "Branco 2 (B2)", "Preto 1 (P1)", "Preto 2 (P2)"]
 
# Posições Iniciais: [B1, B2, P1, P2]
posicoes_iniciais = [1, 3, 7, 9]
 
# Pilhas para a solução efetiva
pilha_posicoes_do_caminho = [posicoes_iniciais]
pilha_movimentos_do_caminho = ["Estado Inicial"]
 
# Contadores de execução
total_becos_sem_saida = 0
total_vezes_que_desfez_jogada = 0
 
 
def posicoes_sao_solucao(posicoes):
    """TESTE DE OBJETIVO: Brancos em {7, 9} e Pretos em {1, 3}"""
    casas_das_brancas = {posicoes[0], posicoes[1]}
    casas_das_pretas = {posicoes[2], posicoes[3]}
    return casas_das_brancas == {7, 9} and casas_das_pretas == {1, 3}
 
 
def buscar_solucao(posicoes_atuais, profundidade_maxima=20):
    global total_becos_sem_saida, total_vezes_que_desfez_jogada
 
    # 1. TESTE DE OBJETIVO
    if posicoes_sao_solucao(posicoes_atuais):
        return True
 
    # 2. IMPASSE POR PROFUNDIDADE (Limite)
    if len(pilha_posicoes_do_caminho) >= profundidade_maxima:
        total_becos_sem_saida += 1
        return False
 
    # 3. GERAÇÃO DE MOVIMENTOS (Apenas a próxima casa no sentido horário)
    for indice_peca in range(4):
        casa_de_origem = posicoes_atuais[indice_peca]
        casa_de_destino = PROXIMA_CASA_HORARIO[casa_de_origem]  # destino único, sentido horário
 
        # Condição 1: Casa de destino VAZIA
        if casa_de_destino not in posicoes_atuais:
            posicoes_apos_mover = list(posicoes_atuais)
            posicoes_apos_mover[indice_peca] = casa_de_destino
  
            # Condição 2: CORTE DE CICLOS (evita repetição no caminho)
            if posicoes_apos_mover not in pilha_posicoes_do_caminho:
                descricao_do_movimento = (
                    f"Mover {NOMES_PECAS[indice_peca]} da casa {casa_de_origem} "
                    f"para a casa {casa_de_destino} (Horário)"
                )
 
                # --- AVANÇO ---
                pilha_posicoes_do_caminho.append(posicoes_apos_mover)
                pilha_movimentos_do_caminho.append(descricao_do_movimento)
 
                # Chamada Recursiva
                if buscar_solucao(posicoes_apos_mover, profundidade_maxima):
                    return True
 
                # --- RETROCESSO (DESFAZ O MOVIMENTO EM IMPASSE) ---
                pilha_posicoes_do_caminho.pop()
                pilha_movimentos_do_caminho.pop()
                total_becos_sem_saida += 1
                total_vezes_que_desfez_jogada += 1
 
    # 4. IMPASSE NATURAL (Sem jogadas válidas no nó atual)
    return False
 
 
# ==============================================================================
# EXECUÇÃO E IMPRESSÃO DO RESUMO FINAL
# ==============================================================================
profundidade_maxima_permitida = 17
solucao_encontrada = buscar_solucao(posicoes_iniciais, profundidade_maxima=profundidade_maxima_permitida)
 
if __name__ == "__main__":
    if solucao_encontrada:
        print("=" * 80)
        print(" RESUMO DA EXECUÇÃO - BACKTRACKING (REGRA RESTRITA: SENTIDO HORÁRIO)")
        print("=" * 80)
        print(f" Total de becos sem saída encontrados : {total_becos_sem_saida}")
        print(f" Total de vezes que desfez uma jogada : {total_vezes_que_desfez_jogada}")
        print(f" TOTAL DE PASSOS DA MELHOR SOLUÇÃO    : {len(pilha_posicoes_do_caminho) - 1}")
        print("=" * 80 + "\n")
 
        print("CAMINHO FINAL DA SOLUÇÃO (PASSOS EFETIVOS LIMPOS):")
        print("-" * 80)
        for passo in range(len(pilha_posicoes_do_caminho)):
            posicoes = pilha_posicoes_do_caminho[passo]
            movimento = pilha_movimentos_do_caminho[passo]
            if passo == 0:
                print(f"Passo {passo:02d} [INÍCIO]: {movimento}")
            else:
                print(f"Passo {passo:02d} [REGRA] : {movimento}")
            print(f"         [ESTADO]: B1 na casa {posicoes[0]} | B2 na casa {posicoes[1]} "
                  f"| P1 na casa {posicoes[2]} | P2 na casa {posicoes[3]}")
            print("-" * 80)
    else:
        print(f"\nNenhuma solução encontrada dentro do limite p={profundidade_maxima_permitida} "
              f"com a regra apenas horária.")