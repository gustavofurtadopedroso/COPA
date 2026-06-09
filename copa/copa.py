import random
import os
import time


SELECOES = [
    "Brasil",
    "Argentina",
    "França",
    "Alemanha",
    "Espanha",
    "Inglaterra",
    "Portugal",
    "Uruguai"
]


def limpar_tela():
    """Limpa o terminal para deixar a visualização mais organizada."""
    os.system("cls" if os.name == "nt" else "clear")


def exibir_cabecalho():
    """Mostra o cabeçalho principal do programa."""
    print("=" * 55)
    print("🏆 SIMULADOR DA COPA DO MUNDO 🏆")
    print("=" * 55)


def exibir_menu():
    """Mostra o menu principal."""
    print("\nMENU PRINCIPAL")
    print("1 - Iniciar simulação")
    print("2 - Ver seleções participantes")
    print("3 - Ver regras")
    print("4 - Sair")


def pausar():
    input("\nPressione Enter para voltar ao menu...")


def aguardar_usuario(mensagem, modo_avanco):
    """
    Controla o ritmo da simulação.

    No modo manual, o usuário precisa digitar 1 para avançar.
    No modo automático, o programa espera alguns segundos.
    """
    if modo_avanco == "manual":
        while True:
            print(f"\n{mensagem}")
            print("1 - Continuar")
            opcao = input("Escolha: ").strip()

            if opcao == "1":
                break

            print("\nOpção inválida. Digite 1 para continuar.")

    else:
        segundos = 5
        print(f"\n{mensagem}")
        print(f"Continuando automaticamente em {segundos} segundos...")
        time.sleep(segundos)


def escolher_modo_avanco():
    """Permite escolher se a Copa será manual ou automática."""
    while True:
        limpar_tela()
        exibir_cabecalho()

        print("\nEscolha como os jogos devem avançar:")
        print("1 - Manual: você digita 1 para ir para o próximo jogo")
        print("2 - Automático: os jogos passam depois de alguns segundos")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            return "manual"

        if opcao == "2":
            return "automatico"

        print("\nOpção inválida.")
        time.sleep(2)


def mostrar_selecoes():
    """Mostra a lista de seleções participantes."""
    limpar_tela()
    exibir_cabecalho()

    print("\n🌍 Seleções participantes:\n")

    for numero, selecao in enumerate(SELECOES, start=1):
        print(f"{numero}. {selecao}")


def mostrar_regras():
    """Mostra as regras da mini Copa."""
    limpar_tela()
    exibir_cabecalho()

    print("\n📋 REGRAS DA MINI COPA\n")
    print("- A competição possui 8 seleções.")
    print("- As seleções são divididas em 2 grupos com 4 times cada.")
    print("- Na fase de grupos, todos jogam contra todos dentro do grupo.")
    print("- Vitória vale 3 pontos.")
    print("- Empate vale 1 ponto.")
    print("- Derrota vale 0 ponto.")
    print("- Os 2 melhores de cada grupo avançam para a semifinal.")
    print("- Em jogos eliminatórios, empate será decidido nos pênaltis.")
    print("- O vencedor da final será o grande campeão.")


def criar_tabela(selecoes):
    """Cria uma tabela de classificação zerada."""
    tabela = {}

    for selecao in selecoes:
        tabela[selecao] = {
            "pontos": 0,
            "jogos": 0,
            "vitorias": 0,
            "empates": 0,
            "derrotas": 0,
            "gols_pro": 0,
            "gols_contra": 0,
            "saldo_gols": 0
        }

    return tabela


def simular_placar():
    """Gera um placar aleatório."""
    gols_time_1 = random.randint(0, 4)
    gols_time_2 = random.randint(0, 4)

    return gols_time_1, gols_time_2


def registrar_resultado(tabela, time_1, time_2, gols_1, gols_2):
    """Atualiza a classificação após uma partida."""
    tabela[time_1]["jogos"] += 1
    tabela[time_2]["jogos"] += 1

    tabela[time_1]["gols_pro"] += gols_1
    tabela[time_1]["gols_contra"] += gols_2

    tabela[time_2]["gols_pro"] += gols_2
    tabela[time_2]["gols_contra"] += gols_1

    tabela[time_1]["saldo_gols"] = tabela[time_1]["gols_pro"] - tabela[time_1]["gols_contra"]
    tabela[time_2]["saldo_gols"] = tabela[time_2]["gols_pro"] - tabela[time_2]["gols_contra"]

    if gols_1 > gols_2:
        tabela[time_1]["pontos"] += 3
        tabela[time_1]["vitorias"] += 1
        tabela[time_2]["derrotas"] += 1

    elif gols_2 > gols_1:
        tabela[time_2]["pontos"] += 3
        tabela[time_2]["vitorias"] += 1
        tabela[time_1]["derrotas"] += 1

    else:
        tabela[time_1]["pontos"] += 1
        tabela[time_2]["pontos"] += 1
        tabela[time_1]["empates"] += 1
        tabela[time_2]["empates"] += 1


def gerar_partidas_do_grupo(grupo):
    """Gera todas as partidas possíveis entre as seleções de um grupo."""
    partidas = []

    for i in range(len(grupo)):
        for j in range(i + 1, len(grupo)):
            partidas.append((grupo[i], grupo[j]))

    return partidas


def ordenar_classificacao(tabela):
    """Ordena a tabela por pontos, saldo de gols e gols marcados."""
    return sorted(
        tabela.items(),
        key=lambda item: (
            -item[1]["pontos"],
            -item[1]["saldo_gols"],
            -item[1]["gols_pro"],
            item[0]
        )
    )


def mostrar_classificacao(nome_grupo, tabela):
    """Mostra a classificação atual do grupo."""
    classificacao = ordenar_classificacao(tabela)

    print(f"\n📊 CLASSIFICAÇÃO ATUAL - {nome_grupo}")
    print("-" * 75)
    print(f"{'Pos':<5}{'Seleção':<15}{'Pts':<6}{'J':<4}{'V':<4}{'E':<4}{'D':<4}{'GP':<5}{'GC':<5}{'SG':<5}")
    print("-" * 75)

    for posicao, (selecao, dados) in enumerate(classificacao, start=1):
        print(
            f"{posicao:<5}"
            f"{selecao:<15}"
            f"{dados['pontos']:<6}"
            f"{dados['jogos']:<4}"
            f"{dados['vitorias']:<4}"
            f"{dados['empates']:<4}"
            f"{dados['derrotas']:<4}"
            f"{dados['gols_pro']:<5}"
            f"{dados['gols_contra']:<5}"
            f"{dados['saldo_gols']:<5}"
        )


def mostrar_resultado(time_1, time_2, gols_1, gols_2):
    """Mostra o resultado da partida."""
    print("\n📢 RESULTADO FINAL")
    print("-" * 40)
    print(f"{time_1} {gols_1} x {gols_2} {time_2}")

    if gols_1 > gols_2:
        print(f"\n✅ Vencedor: {time_1}")
    elif gols_2 > gols_1:
        print(f"\n✅ Vencedor: {time_2}")
    else:
        print("\n🤝 A partida terminou empatada.")


def dividir_grupos():
    """Divide as seleções em dois grupos aleatórios."""
    selecoes_embaralhadas = SELECOES.copy()
    random.shuffle(selecoes_embaralhadas)

    grupo_a = selecoes_embaralhadas[:4]
    grupo_b = selecoes_embaralhadas[4:]

    return grupo_a, grupo_b


def simular_fase_de_grupos(modo_avanco):
    """Simula a fase de grupos jogo por jogo."""
    grupo_a, grupo_b = dividir_grupos()

    grupos = {
        "Grupo A": grupo_a,
        "Grupo B": grupo_b
    }

    classificados = []

    limpar_tela()
    exibir_cabecalho()

    print("\n🎙️ A fase de grupos vai começar!")
    print("As seleções entram em campo em busca da classificação.")

    aguardar_usuario("Iniciar fase de grupos?", modo_avanco)

    for nome_grupo, selecoes_do_grupo in grupos.items():
        tabela = criar_tabela(selecoes_do_grupo)
        partidas = gerar_partidas_do_grupo(selecoes_do_grupo)

        limpar_tela()
        exibir_cabecalho()

        print(f"\n🌍 {nome_grupo}")
        print("-" * 40)

        for selecao in selecoes_do_grupo:
            print(f"- {selecao}")

        aguardar_usuario(f"Iniciar jogos do {nome_grupo}?", modo_avanco)

        for numero_jogo, (time_1, time_2) in enumerate(partidas, start=1):
            limpar_tela()
            exibir_cabecalho()

            print(f"\n⚽ {nome_grupo} - Jogo {numero_jogo}")
            print("-" * 40)
            print(f"Próxima partida: {time_1} x {time_2}")

            aguardar_usuario("Iniciar este jogo?", modo_avanco)

            gols_1, gols_2 = simular_placar()
            registrar_resultado(tabela, time_1, time_2, gols_1, gols_2)

            limpar_tela()
            exibir_cabecalho()

            print(f"\n⚽ {nome_grupo} - Jogo {numero_jogo}")
            mostrar_resultado(time_1, time_2, gols_1, gols_2)
            mostrar_classificacao(nome_grupo, tabela)

            aguardar_usuario("Ir para o próximo jogo?", modo_avanco)

        classificacao = ordenar_classificacao(tabela)

        primeiro_colocado = classificacao[0][0]
        segundo_colocado = classificacao[1][0]

        classificados.append(primeiro_colocado)
        classificados.append(segundo_colocado)

        limpar_tela()
        exibir_cabecalho()

        print(f"\n✅ Fim dos jogos do {nome_grupo}!")
        mostrar_classificacao(nome_grupo, tabela)

        print(f"\n🏅 Classificados do {nome_grupo}:")
        print(f"1º - {primeiro_colocado}")
        print(f"2º - {segundo_colocado}")

        aguardar_usuario("Continuar para a próxima etapa?", modo_avanco)

    return classificados


def simular_penaltis(time_1, time_2, modo_avanco):
    """Simula disputa de pênaltis em caso de empate."""
    print("\n🥅 O jogo terminou empatado!")
    print("Teremos disputa de pênaltis.")

    aguardar_usuario("Iniciar disputa de pênaltis?", modo_avanco)

    penaltis_1 = random.randint(3, 5)
    penaltis_2 = random.randint(3, 5)

    while penaltis_1 == penaltis_2:
        penaltis_1 = random.randint(3, 5)
        penaltis_2 = random.randint(3, 5)

    print("\n📢 Resultado dos pênaltis:")
    print(f"{time_1} {penaltis_1} x {penaltis_2} {time_2}")

    if penaltis_1 > penaltis_2:
        vencedor = time_1
    else:
        vencedor = time_2

    print(f"\n✅ {vencedor} venceu nos pênaltis!")

    return vencedor


def simular_jogo_eliminatorio(time_1, time_2, fase, modo_avanco):
    """Simula um jogo eliminatório."""
    limpar_tela()
    exibir_cabecalho()

    print(f"\n🔥 {fase.upper()}")
    print("-" * 40)
    print(f"Próxima partida: {time_1} x {time_2}")

    aguardar_usuario("Iniciar este jogo decisivo?", modo_avanco)

    gols_1, gols_2 = simular_placar()

    limpar_tela()
    exibir_cabecalho()

    print(f"\n🔥 {fase.upper()}")
    mostrar_resultado(time_1, time_2, gols_1, gols_2)

    if gols_1 > gols_2:
        print(f"\n✅ {time_1} avançou!")
        aguardar_usuario("Continuar?", modo_avanco)
        return time_1

    if gols_2 > gols_1:
        print(f"\n✅ {time_2} avançou!")
        aguardar_usuario("Continuar?", modo_avanco)
        return time_2

    vencedor = simular_penaltis(time_1, time_2, modo_avanco)

    aguardar_usuario("Continuar?", modo_avanco)

    return vencedor


def simular_semifinais(classificados, modo_avanco):
    """Simula as semifinais."""
    limpar_tela()
    exibir_cabecalho()

    print("\n🎙️ Chegamos às semifinais!")
    print("Agora cada jogo vale uma vaga na grande final.")

    print("\nClassificados:")
    for selecao in classificados:
        print(f"- {selecao}")

    aguardar_usuario("Começar semifinais?", modo_avanco)

    finalista_1 = simular_jogo_eliminatorio(
        classificados[0],
        classificados[3],
        "Semifinal 1",
        modo_avanco
    )

    finalista_2 = simular_jogo_eliminatorio(
        classificados[2],
        classificados[1],
        "Semifinal 2",
        modo_avanco
    )

    return finalista_1, finalista_2


def simular_final(finalista_1, finalista_2, modo_avanco):
    """Simula a grande final."""
    limpar_tela()
    exibir_cabecalho()

    print("\n🏆 CHEGOU A GRANDE FINAL!")
    print("O estádio está lotado. A torcida está pronta. Vale o título!")

    print(f"\nFinalistas: {finalista_1} x {finalista_2}")

    aguardar_usuario("Começar a grande final?", modo_avanco)

    campeao = simular_jogo_eliminatorio(
        finalista_1,
        finalista_2,
        "Grande Final",
        modo_avanco
    )

    return campeao


def iniciar_simulacao():
    """Controla a simulação completa da Copa."""
    modo_avanco = escolher_modo_avanco()

    limpar_tela()
    exibir_cabecalho()

    print("\n🎉 Bem-vindo ao Simulador da Copa!")
    print("Agora a Copa será acompanhada com calma, jogo por jogo.")

    print("\n🌍 Seleções participantes:")
    for selecao in SELECOES:
        print(f"- {selecao}")

    aguardar_usuario("Iniciar a Copa?", modo_avanco)

    classificados = simular_fase_de_grupos(modo_avanco)
    finalista_1, finalista_2 = simular_semifinais(classificados, modo_avanco)
    campeao = simular_final(finalista_1, finalista_2, modo_avanco)

    limpar_tela()
    exibir_cabecalho()

    print("\n🎊 FIM DE COPA!")
    print("=" * 55)
    print(f"🏆 CAMPEÃO DA COPA: {campeao.upper()} 🏆")
    print("=" * 55)

    print("\nParabéns ao campeão! Campanha histórica!")


def main():
    """Função principal do programa."""
    while True:
        limpar_tela()
        exibir_cabecalho()
        exibir_menu()

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            iniciar_simulacao()
            pausar()

        elif opcao == "2":
            mostrar_selecoes()
            pausar()

        elif opcao == "3":
            mostrar_regras()
            pausar()

        elif opcao == "4":
            print("\nObrigado por jogar o Simulador da Copa! Até a próxima! 🏆")
            break

        else:
            print("\nOpção inválida. Digite apenas 1, 2, 3 ou 4.")
            time.sleep(2)


if __name__ == "__main__":
    main()