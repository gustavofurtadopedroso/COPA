import pygame
import random
import sys


# =========================
# CONFIGURAÇÕES
# =========================

FPS = 60
LARGURA_JANELA = 1100
ALTURA_JANELA = 700

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

PERGUNTAS_QUIZ = [
    {
        "pergunta": "Em que ano o Brasil conquistou sua primeira Copa do Mundo?",
        "opcoes": ["1950", "1958", "1962", "1970"],
        "resposta": 1
    },
    {
        "pergunta": "Qual seleção tem mais títulos de Copa do Mundo?",
        "opcoes": ["Alemanha", "Argentina", "Brasil", "Itália"],
        "resposta": 2
    },
    {
        "pergunta": "Quem é conhecido como 'O Fenômeno' no futebol brasileiro?",
        "opcoes": ["Romário", "Ronaldo", "Ronaldinho", "Rivaldo"],
        "resposta": 1
    },
    {
        "pergunta": "Em qual país aconteceu a Copa do Mundo de 2014?",
        "opcoes": ["África do Sul", "Rússia", "Brasil", "Alemanha"],
        "resposta": 2
    },
    {
        "pergunta": "Qual foi o placar da final da Copa de 2002 entre Brasil e Alemanha?",
        "opcoes": ["1 x 0", "2 x 0", "3 x 1", "4 x 2"],
        "resposta": 1
    },
    {
        "pergunta": "Quem foi o capitão do Brasil na conquista da Copa de 1994?",
        "opcoes": ["Cafu", "Dunga", "Romário", "Bebeto"],
        "resposta": 1
    },
    {
        "pergunta": "Qual jogador brasileiro marcou dois gols na final da Copa de 1958?",
        "opcoes": ["Pelé", "Garrincha", "Zagallo", "Vavá"],
        "resposta": 0
    },
    {
        "pergunta": "Quantas seleções normalmente existem em um grupo da Copa do Mundo?",
        "opcoes": ["2", "3", "4", "5"],
        "resposta": 2
    }
]


# =========================
# CORES
# =========================

AZUL_ESCURO = (13, 27, 42)
AZUL = (27, 78, 155)
AZUL_CLARO = (58, 134, 255)
AMARELO = (255, 202, 58)
VERDE = (36, 173, 95)
VERMELHO = (230, 57, 70)
BRANCO = (245, 245, 245)
PRETO = (15, 15, 15)
CINZA = (210, 210, 210)
CINZA_ESCURO = (55, 65, 81)
CARD = (24, 49, 83)


# =========================
# FUNÇÕES AUXILIARES
# =========================

def criar_fonte(tamanho, negrito=False):
    return pygame.font.SysFont("arial", tamanho, bold=negrito)


def desenhar_texto(tela, texto, tamanho, x, y, cor=BRANCO, centro=False, negrito=False):
    fonte = criar_fonte(tamanho, negrito)
    imagem = fonte.render(texto, True, cor)
    retangulo = imagem.get_rect()

    if centro:
        retangulo.center = (x, y)
    else:
        retangulo.topleft = (x, y)

    tela.blit(imagem, retangulo)


def desenhar_texto_quebrado(tela, texto, tamanho, x, y, largura_maxima, cor=BRANCO):
    fonte = criar_fonte(tamanho)
    palavras = texto.split()
    linha = ""
    linhas = []

    for palavra in palavras:
        teste = linha + palavra + " "

        if fonte.size(teste)[0] <= largura_maxima:
            linha = teste
        else:
            linhas.append(linha)
            linha = palavra + " "

    linhas.append(linha)

    for linha_texto in linhas:
        imagem = fonte.render(linha_texto.strip(), True, cor)
        tela.blit(imagem, (x, y))
        y += tamanho + 8

    return y


def simular_placar():
    return random.randint(0, 4), random.randint(0, 4)


def criar_tabela(selecoes):
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


def registrar_resultado(tabela, time_1, time_2, gols_1, gols_2):
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
    partidas = []

    for i in range(len(grupo)):
        for j in range(i + 1, len(grupo)):
            partidas.append((grupo[i], grupo[j]))

    return partidas


def ordenar_classificacao(tabela):
    return sorted(
        tabela.items(),
        key=lambda item: (
            -item[1]["pontos"],
            -item[1]["saldo_gols"],
            -item[1]["gols_pro"],
            item[0]
        )
    )


# =========================
# BOTÃO
# =========================

class Botao:
    def __init__(self, x, y, largura, altura, texto, acao, cor=BRANCO):
        self.retangulo = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.acao = acao
        self.cor = cor

    def desenhar(self, tela):
        mouse = pygame.mouse.get_pos()

        if self.retangulo.collidepoint(mouse):
            cor_botao = AMARELO
            cor_texto = PRETO
        else:
            cor_botao = self.cor
            cor_texto = PRETO

        pygame.draw.rect(tela, cor_botao, self.retangulo, border_radius=14)
        pygame.draw.rect(tela, PRETO, self.retangulo, 2, border_radius=14)

        desenhar_texto(
            tela,
            self.texto,
            23,
            self.retangulo.centerx,
            self.retangulo.centery,
            cor_texto,
            centro=True,
            negrito=True
        )

    def clicou(self, posicao):
        return self.retangulo.collidepoint(posicao)


# =========================
# JOGO
# =========================

class SimuladorCopa:
    def __init__(self, tela):
        self.tela = tela
        self.largura, self.altura = tela.get_size()

        self.tela_atual = "menu"
        self.botoes = []

        self.grupos = {}
        self.ordem_grupos = []
        self.tabelas = {}
        self.partidas_grupos = {}

        self.indice_grupo = 0
        self.indice_jogo = 0

        self.classificados = []
        self.finalistas = []
        self.campeao = None

        self.partida_atual = None
        self.resultado_atual = None

        self.fase_mata_mata = ""
        self.partidas_mata_mata = []
        self.indice_mata_mata = 0

        self.indice_pergunta = 0
        self.pontos_quiz = 0
        self.resposta_marcada = None
        self.quiz_finalizado = False

    # =========================
    # BASE VISUAL
    # =========================

    def atualizar_tamanho(self, tela):
        self.tela = tela
        self.largura, self.altura = tela.get_size()

    def desenhar_fundo(self):
        self.tela.fill(AZUL_ESCURO)

        pygame.draw.circle(self.tela, AZUL, (120, 120), 180)
        pygame.draw.circle(self.tela, VERDE, (self.largura - 120, self.altura - 90), 220)
        pygame.draw.circle(self.tela, AMARELO, (self.largura - 90, 100), 90)

        painel = pygame.Rect(50, 40, self.largura - 100, self.altura - 80)
        pygame.draw.rect(self.tela, CARD, painel, border_radius=28)
        pygame.draw.rect(self.tela, AZUL_CLARO, painel, 3, border_radius=28)

    def titulo(self, texto, subtitulo=""):
        desenhar_texto(
            self.tela,
            texto,
            44,
            self.largura // 2,
            85,
            AMARELO,
            centro=True,
            negrito=True
        )

        if subtitulo:
            desenhar_texto(
                self.tela,
                subtitulo,
                24,
                self.largura // 2,
                130,
                BRANCO,
                centro=True
            )

    def criar_botao(self, x, y, largura, altura, texto, acao, cor=BRANCO):
        botao = Botao(x, y, largura, altura, texto, acao, cor)
        self.botoes.append(botao)
        botao.desenhar(self.tela)

    # =========================
    # MENU
    # =========================

    def desenhar_menu(self):
        self.desenhar_fundo()
        self.titulo("SIMULADOR DA COPA", "Menu principal do jogo")

        centro_x = self.largura // 2
        largura_botao = 310
        altura_botao = 55
        x = centro_x - largura_botao // 2
        y = 190
        espaco = 68

        self.criar_botao(x, y, largura_botao, altura_botao, "Iniciar Copa", self.iniciar_copa)
        self.criar_botao(x, y + espaco, largura_botao, altura_botao, "Ver Seleções", self.ir_para_selecoes)
        self.criar_botao(x, y + espaco * 2, largura_botao, altura_botao, "Ver Regras", self.ir_para_regras)
        self.criar_botao(x, y + espaco * 3, largura_botao, altura_botao, "Quiz da Copa", self.iniciar_quiz)
        self.criar_botao(x, y + espaco * 4, largura_botao, altura_botao, "Sair", self.sair, VERMELHO)

        desenhar_texto(
            self.tela,
            "F11: alternar tela cheia | ESC: sair",
            20,
            centro_x,
            self.altura - 75,
            CINZA,
            centro=True
        )

    def desenhar_selecoes(self):
        self.desenhar_fundo()
        self.titulo("SELEÇÕES PARTICIPANTES")

        x = self.largura // 2 - 170
        y = 180

        for i, selecao in enumerate(SELECOES, start=1):
            desenhar_texto(self.tela, f"{i}. {selecao}", 30, x, y, BRANCO)
            y += 45

        self.criar_botao(self.largura // 2 - 150, self.altura - 110, 300, 55, "Voltar", self.ir_para_menu)

    def desenhar_regras(self):
        self.desenhar_fundo()
        self.titulo("REGRAS DA COPA")

        regras = [
            "A competição tem 8 seleções.",
            "As seleções são divididas em 2 grupos.",
            "Cada grupo tem 4 seleções.",
            "Todos jogam contra todos dentro do grupo.",
            "Vitória vale 3 pontos.",
            "Empate vale 1 ponto.",
            "Os 2 melhores de cada grupo vão para a semifinal.",
            "No mata-mata, empate vai para os pênaltis.",
            "O vencedor da final será o campeão."
        ]

        x = 140
        y = 170

        for regra in regras:
            desenhar_texto(self.tela, f"- {regra}", 24, x, y, BRANCO)
            y += 38

        self.criar_botao(self.largura // 2 - 150, self.altura - 110, 300, 55, "Voltar", self.ir_para_menu)

    # =========================
    # QUIZ
    # =========================

    def iniciar_quiz(self):
        self.indice_pergunta = 0
        self.pontos_quiz = 0
        self.resposta_marcada = None
        self.quiz_finalizado = False
        self.tela_atual = "quiz"

    def desenhar_quiz(self):
        self.desenhar_fundo()
        self.titulo("QUIZ DA COPA", "Perguntas gerais com ênfase no Brasil")

        if self.indice_pergunta >= len(PERGUNTAS_QUIZ):
            self.desenhar_resultado_quiz()
            return

        pergunta_atual = PERGUNTAS_QUIZ[self.indice_pergunta]

        desenhar_texto(
            self.tela,
            f"Pergunta {self.indice_pergunta + 1} de {len(PERGUNTAS_QUIZ)}",
            24,
            self.largura // 2,
            165,
            AMARELO,
            centro=True,
            negrito=True
        )

        desenhar_texto_quebrado(
            self.tela,
            pergunta_atual["pergunta"],
            30,
            140,
            210,
            self.largura - 280,
            BRANCO
        )

        opcoes = pergunta_atual["opcoes"]

        largura_botao = min(700, self.largura - 260)
        x = self.largura // 2 - largura_botao // 2
        y = 330

        for indice, opcao in enumerate(opcoes):
            texto = f"{indice + 1}. {opcao}"
            self.criar_botao(
                x,
                y + indice * 65,
                largura_botao,
                52,
                texto,
                lambda i=indice: self.responder_quiz(i)
            )

        self.criar_botao(80, self.altura - 100, 220, 50, "Voltar ao Menu", self.ir_para_menu)

        desenhar_texto(
            self.tela,
            f"Pontuação: {self.pontos_quiz}",
            24,
            self.largura - 210,
            self.altura - 88,
            BRANCO
        )

    def responder_quiz(self, indice_resposta):
        pergunta_atual = PERGUNTAS_QUIZ[self.indice_pergunta]

        if indice_resposta == pergunta_atual["resposta"]:
            self.pontos_quiz += 1

        self.indice_pergunta += 1

    def desenhar_resultado_quiz(self):
        self.titulo("RESULTADO DO QUIZ")

        total = len(PERGUNTAS_QUIZ)

        desenhar_texto(
            self.tela,
            f"Você acertou {self.pontos_quiz} de {total} perguntas.",
            36,
            self.largura // 2,
            240,
            BRANCO,
            centro=True,
            negrito=True
        )

        if self.pontos_quiz == total:
            mensagem = "Perfeito! Você entende muito de Copa do Mundo."
        elif self.pontos_quiz >= total // 2:
            mensagem = "Muito bem! Você conhece bastante sobre Copa."
        else:
            mensagem = "Boa tentativa! Vale estudar mais a história da Copa."

        desenhar_texto(
            self.tela,
            mensagem,
            28,
            self.largura // 2,
            310,
            AMARELO,
            centro=True
        )

        self.criar_botao(self.largura // 2 - 320, 430, 280, 55, "Jogar Quiz de Novo", self.iniciar_quiz)
        self.criar_botao(self.largura // 2 + 40, 430, 280, 55, "Voltar ao Menu", self.ir_para_menu)

    # =========================
    # COPA
    # =========================

    def iniciar_copa(self):
        selecoes_sorteadas = SELECOES.copy()
        random.shuffle(selecoes_sorteadas)

        grupo_a = selecoes_sorteadas[:4]
        grupo_b = selecoes_sorteadas[4:]

        self.grupos = {
            "Grupo A": grupo_a,
            "Grupo B": grupo_b
        }

        self.ordem_grupos = ["Grupo A", "Grupo B"]

        self.tabelas = {
            "Grupo A": criar_tabela(grupo_a),
            "Grupo B": criar_tabela(grupo_b)
        }

        self.partidas_grupos = {
            "Grupo A": gerar_partidas_do_grupo(grupo_a),
            "Grupo B": gerar_partidas_do_grupo(grupo_b)
        }

        self.indice_grupo = 0
        self.indice_jogo = 0
        self.classificados = []
        self.finalistas = []
        self.campeao = None
        self.resultado_atual = None

        self.tela_atual = "intro_grupos"

    def desenhar_intro_grupos(self):
        self.desenhar_fundo()
        self.titulo("A COPA VAI COMEÇAR", "Os grupos foram sorteados")

        x_a = self.largura // 2 - 320
        x_b = self.largura // 2 + 100
        y = 210

        desenhar_texto(self.tela, "Grupo A", 32, x_a, y, AMARELO, negrito=True)
        desenhar_texto(self.tela, "Grupo B", 32, x_b, y, AMARELO, negrito=True)

        for i, selecao in enumerate(self.grupos["Grupo A"]):
            desenhar_texto(self.tela, f"- {selecao}", 25, x_a, y + 55 + i * 38)

        for i, selecao in enumerate(self.grupos["Grupo B"]):
            desenhar_texto(self.tela, f"- {selecao}", 25, x_b, y + 55 + i * 38)

        self.criar_botao(self.largura // 2 - 170, self.altura - 120, 340, 60, "Começar Fase de Grupos", self.ir_para_intro_grupo)

    def ir_para_intro_grupo(self):
        self.tela_atual = "intro_grupo"

    def desenhar_intro_grupo(self):
        self.desenhar_fundo()

        nome_grupo = self.ordem_grupos[self.indice_grupo]
        self.titulo(nome_grupo, "Clique para iniciar os jogos deste grupo")

        y = 220
        for selecao in self.grupos[nome_grupo]:
            desenhar_texto(self.tela, f"- {selecao}", 32, self.largura // 2 - 110, y)
            y += 50

        self.criar_botao(self.largura // 2 - 150, self.altura - 120, 300, 60, "Iniciar Jogos", self.preparar_jogo_grupo)

    def preparar_jogo_grupo(self):
        nome_grupo = self.ordem_grupos[self.indice_grupo]
        partidas = self.partidas_grupos[nome_grupo]

        if self.indice_jogo < len(partidas):
            self.partida_atual = partidas[self.indice_jogo]
            self.resultado_atual = None
            self.tela_atual = "jogo_grupo_antes"
        else:
            self.tela_atual = "grupo_finalizado"

    def desenhar_jogo_grupo_antes(self):
        self.desenhar_fundo()

        nome_grupo = self.ordem_grupos[self.indice_grupo]
        time_1, time_2 = self.partida_atual

        self.titulo(f"{nome_grupo} - Jogo {self.indice_jogo + 1}")

        desenhar_texto(self.tela, "Próxima partida:", 30, self.largura // 2, 230, centro=True)
        desenhar_texto(self.tela, f"{time_1}  x  {time_2}", 48, self.largura // 2, 305, AMARELO, centro=True, negrito=True)

        self.criar_botao(self.largura // 2 - 150, 430, 300, 60, "Simular Jogo", self.simular_jogo_grupo)

    def simular_jogo_grupo(self):
        nome_grupo = self.ordem_grupos[self.indice_grupo]
        tabela = self.tabelas[nome_grupo]

        time_1, time_2 = self.partida_atual
        gols_1, gols_2 = simular_placar()

        registrar_resultado(tabela, time_1, time_2, gols_1, gols_2)

        self.resultado_atual = {
            "time_1": time_1,
            "time_2": time_2,
            "gols_1": gols_1,
            "gols_2": gols_2
        }

        self.tela_atual = "jogo_grupo_depois"

    def desenhar_resultado_jogo(self, x, y):
        resultado = self.resultado_atual

        time_1 = resultado["time_1"]
        time_2 = resultado["time_2"]
        gols_1 = resultado["gols_1"]
        gols_2 = resultado["gols_2"]

        desenhar_texto(self.tela, "Resultado", 30, x, y, AMARELO, negrito=True)
        desenhar_texto(self.tela, f"{time_1} {gols_1} x {gols_2} {time_2}", 35, x, y + 55, BRANCO, negrito=True)

        if gols_1 > gols_2:
            mensagem = f"Vencedor: {time_1}"
        elif gols_2 > gols_1:
            mensagem = f"Vencedor: {time_2}"
        else:
            mensagem = "Empate"

        desenhar_texto(self.tela, mensagem, 25, x, y + 110, BRANCO)

    def desenhar_classificacao(self, nome_grupo, x, y):
        tabela = self.tabelas[nome_grupo]
        classificacao = ordenar_classificacao(tabela)

        desenhar_texto(self.tela, f"Classificação - {nome_grupo}", 28, x, y, AMARELO, negrito=True)

        cabecalho = "Pos  Seleção        Pts  J  V  E  D  SG"
        desenhar_texto(self.tela, cabecalho, 20, x, y + 45, BRANCO, negrito=True)

        y_linha = y + 80

        for pos, (selecao, dados) in enumerate(classificacao, start=1):
            linha = (
                f"{pos:<5}"
                f"{selecao:<15}"
                f"{dados['pontos']:<5}"
                f"{dados['jogos']:<3}"
                f"{dados['vitorias']:<3}"
                f"{dados['empates']:<3}"
                f"{dados['derrotas']:<3}"
                f"{dados['saldo_gols']:<3}"
            )

            desenhar_texto(self.tela, linha, 20, x, y_linha, BRANCO)
            y_linha += 32

    def desenhar_jogo_grupo_depois(self):
        self.desenhar_fundo()

        nome_grupo = self.ordem_grupos[self.indice_grupo]
        self.titulo(f"{nome_grupo} - Resultado")

        self.desenhar_resultado_jogo(110, 200)
        self.desenhar_classificacao(nome_grupo, self.largura // 2 + 60, 190)

        total_partidas = len(self.partidas_grupos[nome_grupo])

        if self.indice_jogo == total_partidas - 1:
            texto_botao = "Ver Classificados"
        else:
            texto_botao = "Próximo Jogo"

        self.criar_botao(self.largura // 2 - 150, self.altura - 110, 300, 55, texto_botao, self.avancar_jogo_grupo)

    def avancar_jogo_grupo(self):
        self.indice_jogo += 1
        self.preparar_jogo_grupo()

    def desenhar_grupo_finalizado(self):
        self.desenhar_fundo()

        nome_grupo = self.ordem_grupos[self.indice_grupo]
        classificacao = ordenar_classificacao(self.tabelas[nome_grupo])

        primeiro = classificacao[0][0]
        segundo = classificacao[1][0]

        if primeiro not in self.classificados:
            self.classificados.append(primeiro)
            self.classificados.append(segundo)

        self.titulo(f"{nome_grupo} finalizado")

        self.desenhar_classificacao(nome_grupo, self.largura // 2 - 230, 180)

        desenhar_texto(self.tela, "Classificados:", 30, self.largura // 2, 445, AMARELO, centro=True, negrito=True)
        desenhar_texto(self.tela, f"1º {primeiro}", 27, self.largura // 2, 490, BRANCO, centro=True)
        desenhar_texto(self.tela, f"2º {segundo}", 27, self.largura // 2, 530, BRANCO, centro=True)

        if self.indice_grupo == 0:
            self.criar_botao(self.largura // 2 - 150, self.altura - 90, 300, 50, "Ir para Grupo B", self.ir_para_proximo_grupo)
        else:
            self.criar_botao(self.largura // 2 - 150, self.altura - 90, 300, 50, "Ir para Semifinais", self.iniciar_semifinais)

    def ir_para_proximo_grupo(self):
        self.indice_grupo += 1
        self.indice_jogo = 0
        self.tela_atual = "intro_grupo"

    # =========================
    # MATA-MATA
    # =========================

    def iniciar_semifinais(self):
        self.fase_mata_mata = "semifinal"
        self.partidas_mata_mata = [
            ("Semifinal 1", self.classificados[0], self.classificados[3]),
            ("Semifinal 2", self.classificados[2], self.classificados[1])
        ]

        self.indice_mata_mata = 0
        self.finalistas = []
        self.tela_atual = "intro_semifinais"

    def desenhar_intro_semifinais(self):
        self.desenhar_fundo()
        self.titulo("SEMIFINAIS", "Agora é mata-mata")

        y = 240

        for fase, time_1, time_2 in self.partidas_mata_mata:
            desenhar_texto(self.tela, f"{fase}: {time_1} x {time_2}", 32, self.largura // 2, y, AMARELO, centro=True)
            y += 65

        self.criar_botao(self.largura // 2 - 160, self.altura - 130, 320, 60, "Começar Semifinais", self.preparar_mata_mata)

    def preparar_mata_mata(self):
        self.resultado_atual = None
        self.tela_atual = "mata_mata_antes"

    def desenhar_mata_mata_antes(self):
        self.desenhar_fundo()

        fase, time_1, time_2 = self.partidas_mata_mata[self.indice_mata_mata]

        self.titulo(fase)

        desenhar_texto(self.tela, "Jogo decisivo:", 30, self.largura // 2, 230, centro=True)
        desenhar_texto(self.tela, f"{time_1}  x  {time_2}", 48, self.largura // 2, 305, AMARELO, centro=True, negrito=True)

        self.criar_botao(self.largura // 2 - 150, 430, 300, 60, "Simular Jogo", self.simular_mata_mata)

    def simular_penaltis(self, time_1, time_2):
        penaltis_1 = random.randint(3, 5)
        penaltis_2 = random.randint(3, 5)

        while penaltis_1 == penaltis_2:
            penaltis_1 = random.randint(3, 5)
            penaltis_2 = random.randint(3, 5)

        vencedor = time_1 if penaltis_1 > penaltis_2 else time_2
        return penaltis_1, penaltis_2, vencedor

    def simular_mata_mata(self):
        fase, time_1, time_2 = self.partidas_mata_mata[self.indice_mata_mata]

        gols_1, gols_2 = simular_placar()
        penaltis_1 = None
        penaltis_2 = None

        if gols_1 > gols_2:
            vencedor = time_1
        elif gols_2 > gols_1:
            vencedor = time_2
        else:
            penaltis_1, penaltis_2, vencedor = self.simular_penaltis(time_1, time_2)

        self.resultado_atual = {
            "fase": fase,
            "time_1": time_1,
            "time_2": time_2,
            "gols_1": gols_1,
            "gols_2": gols_2,
            "penaltis_1": penaltis_1,
            "penaltis_2": penaltis_2,
            "vencedor": vencedor
        }

        if self.fase_mata_mata == "semifinal":
            self.finalistas.append(vencedor)
        else:
            self.campeao = vencedor

        self.tela_atual = "mata_mata_depois"

    def desenhar_mata_mata_depois(self):
        self.desenhar_fundo()

        r = self.resultado_atual

        self.titulo(r["fase"])

        desenhar_texto(
            self.tela,
            f"{r['time_1']} {r['gols_1']} x {r['gols_2']} {r['time_2']}",
            48,
            self.largura // 2,
            235,
            BRANCO,
            centro=True,
            negrito=True
        )

        y = 315

        if r["penaltis_1"] is not None:
            desenhar_texto(self.tela, "Empate no tempo normal. Decisão nos pênaltis:", 27, self.largura // 2, y, centro=True)
            y += 55
            desenhar_texto(
                self.tela,
                f"{r['time_1']} {r['penaltis_1']} x {r['penaltis_2']} {r['time_2']}",
                34,
                self.largura // 2,
                y,
                AMARELO,
                centro=True,
                negrito=True
            )
            y += 70

        desenhar_texto(
            self.tela,
            f"Classificado: {r['vencedor']}",
            34,
            self.largura // 2,
            y,
            AMARELO,
            centro=True,
            negrito=True
        )

        if self.fase_mata_mata == "semifinal":
            if self.indice_mata_mata == 0:
                texto = "Próxima Semifinal"
            else:
                texto = "Ir para Final"
        else:
            texto = "Ver Campeão"

        self.criar_botao(self.largura // 2 - 150, self.altura - 110, 300, 55, texto, self.avancar_mata_mata)

    def avancar_mata_mata(self):
        if self.fase_mata_mata == "semifinal":
            self.indice_mata_mata += 1

            if self.indice_mata_mata < len(self.partidas_mata_mata):
                self.tela_atual = "mata_mata_antes"
            else:
                self.tela_atual = "intro_final"
        else:
            self.tela_atual = "campeao"

    def desenhar_intro_final(self):
        self.desenhar_fundo()
        self.titulo("GRANDE FINAL", "Vale o título da Copa")

        desenhar_texto(
            self.tela,
            f"{self.finalistas[0]}  x  {self.finalistas[1]}",
            52,
            self.largura // 2,
            300,
            AMARELO,
            centro=True,
            negrito=True
        )

        self.criar_botao(self.largura // 2 - 150, 430, 300, 60, "Começar Final", self.iniciar_final)

    def iniciar_final(self):
        self.fase_mata_mata = "final"
        self.partidas_mata_mata = [
            ("Grande Final", self.finalistas[0], self.finalistas[1])
        ]
        self.indice_mata_mata = 0
        self.tela_atual = "mata_mata_antes"

    def desenhar_campeao(self):
        self.desenhar_fundo()
        self.titulo("FIM DE COPA")

        desenhar_texto(self.tela, "CAMPEÃO", 44, self.largura // 2, 230, AMARELO, centro=True, negrito=True)
        desenhar_texto(self.tela, self.campeao.upper(), 64, self.largura // 2, 320, BRANCO, centro=True, negrito=True)

        self.criar_botao(self.largura // 2 - 310, 480, 280, 55, "Nova Copa", self.iniciar_copa)
        self.criar_botao(self.largura // 2 + 30, 480, 280, 55, "Menu", self.ir_para_menu)

    # =========================
    # NAVEGAÇÃO
    # =========================

    def ir_para_menu(self):
        self.tela_atual = "menu"

    def ir_para_selecoes(self):
        self.tela_atual = "selecoes"

    def ir_para_regras(self):
        self.tela_atual = "regras"

    def sair(self):
        pygame.quit()
        sys.exit()

    # =========================
    # DESENHO E EVENTOS
    # =========================

    def desenhar(self):
        self.botoes = []

        if self.tela_atual == "menu":
            self.desenhar_menu()
        elif self.tela_atual == "selecoes":
            self.desenhar_selecoes()
        elif self.tela_atual == "regras":
            self.desenhar_regras()
        elif self.tela_atual == "quiz":
            self.desenhar_quiz()
        elif self.tela_atual == "intro_grupos":
            self.desenhar_intro_grupos()
        elif self.tela_atual == "intro_grupo":
            self.desenhar_intro_grupo()
        elif self.tela_atual == "jogo_grupo_antes":
            self.desenhar_jogo_grupo_antes()
        elif self.tela_atual == "jogo_grupo_depois":
            self.desenhar_jogo_grupo_depois()
        elif self.tela_atual == "grupo_finalizado":
            self.desenhar_grupo_finalizado()
        elif self.tela_atual == "intro_semifinais":
            self.desenhar_intro_semifinais()
        elif self.tela_atual == "mata_mata_antes":
            self.desenhar_mata_mata_antes()
        elif self.tela_atual == "mata_mata_depois":
            self.desenhar_mata_mata_depois()
        elif self.tela_atual == "intro_final":
            self.desenhar_intro_final()
        elif self.tela_atual == "campeao":
            self.desenhar_campeao()


# =========================
# EXECUÇÃO
# =========================

def criar_tela(tela_cheia):
    if tela_cheia:
        return pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    return pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA), pygame.RESIZABLE)


def main():
    pygame.init()

    tela_cheia = True
    tela = criar_tela(tela_cheia)

    pygame.display.set_caption("Simulador da Copa")

    relogio = pygame.time.Clock()
    jogo = SimuladorCopa(tela)

    while True:
        jogo.desenhar()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jogo.sair()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    jogo.sair()

                if evento.key == pygame.K_F11:
                    tela_cheia = not tela_cheia
                    tela = criar_tela(tela_cheia)
                    jogo.atualizar_tamanho(tela)

            if evento.type == pygame.VIDEORESIZE and not tela_cheia:
                tela = pygame.display.set_mode((evento.w, evento.h), pygame.RESIZABLE)
                jogo.atualizar_tamanho(tela)

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                posicao = pygame.mouse.get_pos()

                for botao in jogo.botoes:
                    if botao.clicou(posicao):
                        botao.acao()
                        break

        pygame.display.flip()
        relogio.tick(FPS)


if __name__ == "__main__":
    main()