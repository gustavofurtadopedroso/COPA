"""
Simulador da Copa do Mundo 2026
Projeto em Python com Pygame.

Mini sistema com:
- Menu principal;
- Simulação de uma mini Copa 2026;
- Fase de grupos;
- Classificação automática;
- Quartas, semifinais e final;
- Decisão por pênaltis;
- Quiz temático sobre Copa do Mundo;
- Interface gráfica com botões;
- Tela cheia com F11.

Autor: Gustavo Furtado Pedroso
"""

import random
import sys
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Tuple

import pygame


# =========================================================
# CONFIGURAÇÕES GERAIS
# =========================================================

LARGURA_INICIAL = 1180
ALTURA_INICIAL = 720
FPS = 60

TITULO_JANELA = "Simulador da Copa do Mundo 2026"

# Paleta visual
AZUL_ESCURO = (8, 20, 45)
AZUL_MEDIO = (17, 47, 91)
AZUL_CLARO = (58, 134, 255)
VERDE = (38, 166, 91)
VERDE_CLARO = (77, 214, 128)
AMARELO = (255, 205, 60)
LARANJA = (255, 159, 67)
VERMELHO = (225, 55, 65)
BRANCO = (245, 247, 250)
CINZA = (190, 198, 210)
CINZA_ESCURO = (44, 55, 73)
PRETO = (12, 14, 20)
CARD = (20, 42, 78)
CARD_2 = (28, 55, 98)


# =========================================================
# DADOS DO JOGO
# =========================================================

# Seleções usadas na simulação. Não representa necessariamente os grupos reais.
SELECOES = [
    {"nome": "Brasil", "forca": 92},
    {"nome": "Argentina", "forca": 90},
    {"nome": "França", "forca": 91},
    {"nome": "Alemanha", "forca": 88},
    {"nome": "Espanha", "forca": 89},
    {"nome": "Inglaterra", "forca": 88},
    {"nome": "Portugal", "forca": 87},
    {"nome": "Uruguai", "forca": 84},
    {"nome": "Holanda", "forca": 86},
    {"nome": "Croácia", "forca": 82},
    {"nome": "Bélgica", "forca": 83},
    {"nome": "Japão", "forca": 78},
    {"nome": "México", "forca": 77},
    {"nome": "Estados Unidos", "forca": 76},
    {"nome": "Canadá", "forca": 73},
    {"nome": "Marrocos", "forca": 80},
]

PERGUNTAS_QUIZ = [
    {
        "pergunta": "Em que ano o Brasil conquistou sua primeira Copa do Mundo?",
        "opcoes": ["1950", "1958", "1962", "1970"],
        "resposta": 1,
    },
    {
        "pergunta": "Qual seleção possui mais títulos de Copa do Mundo?",
        "opcoes": ["Alemanha", "Argentina", "Brasil", "Itália"],
        "resposta": 2,
    },
    {
        "pergunta": "Quem é conhecido como 'O Fenômeno' no futebol brasileiro?",
        "opcoes": ["Romário", "Ronaldo", "Ronaldinho", "Rivaldo"],
        "resposta": 1,
    },
    {
        "pergunta": "Em qual país aconteceu a Copa do Mundo de 2014?",
        "opcoes": ["África do Sul", "Rússia", "Brasil", "Alemanha"],
        "resposta": 2,
    },
    {
        "pergunta": "Qual foi o placar da final da Copa de 2002 entre Brasil e Alemanha?",
        "opcoes": ["1 x 0", "2 x 0", "3 x 1", "4 x 2"],
        "resposta": 1,
    },
    {
        "pergunta": "Quem foi o capitão do Brasil na conquista da Copa de 1994?",
        "opcoes": ["Cafu", "Dunga", "Romário", "Bebeto"],
        "resposta": 1,
    },
    {
        "pergunta": "Qual jogador brasileiro marcou dois gols na final da Copa de 1958?",
        "opcoes": ["Pelé", "Garrincha", "Zagallo", "Vavá"],
        "resposta": 0,
    },
    {
        "pergunta": "Na fase de grupos, qual resultado normalmente dá 3 pontos?",
        "opcoes": ["Empate", "Vitória", "Derrota", "Jogo cancelado"],
        "resposta": 1,
    },
    {
        "pergunta": "O que acontece em uma partida eliminatória se houver empate no tempo normal?",
        "opcoes": ["Ambos avançam", "Sorteio", "Decisão por pênaltis", "O time com mais posse avança"],
        "resposta": 2,
    },
    {
        "pergunta": "Qual edição da Copa é o tema principal deste projeto?",
        "opcoes": ["2014", "2018", "2022", "2026"],
        "resposta": 3,
    },
]


# =========================================================
# ESTRUTURAS DE DADOS
# =========================================================

@dataclass
class Resultado:
    time_1: str
    time_2: str
    gols_1: int
    gols_2: int
    vencedor: Optional[str] = None
    penaltis_1: Optional[int] = None
    penaltis_2: Optional[int] = None


TabelaTime = Dict[str, int]
TabelaGrupo = Dict[str, TabelaTime]
PartidaGrupo = Tuple[str, str, str]  # grupo, time_1, time_2
PartidaMataMata = Tuple[str, str, str]  # fase, time_1, time_2


# =========================================================
# FUNÇÕES AUXILIARES
# =========================================================

def obter_fonte(tamanho: int, negrito: bool = False) -> pygame.font.Font:
    return pygame.font.SysFont("arial", tamanho, bold=negrito)


def texto(tela: pygame.Surface, conteudo: str, tamanho: int, x: int, y: int,
          cor=BRANCO, centro: bool = False, negrito: bool = False) -> pygame.Rect:
    fonte = obter_fonte(tamanho, negrito)
    imagem = fonte.render(conteudo, True, cor)
    rect = imagem.get_rect()
    if centro:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    tela.blit(imagem, rect)
    return rect


def texto_quebrado(tela: pygame.Surface, conteudo: str, tamanho: int, x: int, y: int,
                   largura_maxima: int, cor=BRANCO, negrito: bool = False,
                   espacamento: int = 8) -> int:
    fonte = obter_fonte(tamanho, negrito)
    palavras = conteudo.split()
    linhas: List[str] = []
    linha_atual = ""

    for palavra in palavras:
        teste = (linha_atual + " " + palavra).strip()
        if fonte.size(teste)[0] <= largura_maxima:
            linha_atual = teste
        else:
            if linha_atual:
                linhas.append(linha_atual)
            linha_atual = palavra

    if linha_atual:
        linhas.append(linha_atual)

    for linha in linhas:
        img = fonte.render(linha, True, cor)
        tela.blit(img, (x, y))
        y += tamanho + espacamento

    return y


def criar_tabela(selecoes: List[str]) -> TabelaGrupo:
    tabela: TabelaGrupo = {}
    for selecao in selecoes:
        tabela[selecao] = {
            "pts": 0,
            "j": 0,
            "v": 0,
            "e": 0,
            "d": 0,
            "gp": 0,
            "gc": 0,
            "sg": 0,
        }
    return tabela


def ordenar_tabela(tabela: TabelaGrupo) -> List[Tuple[str, TabelaTime]]:
    return sorted(
        tabela.items(),
        key=lambda item: (
            -item[1]["pts"],
            -item[1]["sg"],
            -item[1]["gp"],
            item[0],
        ),
    )


def gerar_partidas_grupo(grupo_nome: str, selecoes: List[str]) -> List[PartidaGrupo]:
    partidas: List[PartidaGrupo] = []
    for i in range(len(selecoes)):
        for j in range(i + 1, len(selecoes)):
            partidas.append((grupo_nome, selecoes[i], selecoes[j]))
    return partidas


def forca_da_selecao(nome: str) -> int:
    for selecao in SELECOES:
        if selecao["nome"] == nome:
            return int(selecao["forca"])
    return 75


def simular_gols(nome_time: str, forca_adversario: int) -> int:
    """Gera gols levando em conta a força do time e do adversário."""
    forca_time = forca_da_selecao(nome_time)
    diferenca = forca_time - forca_adversario

    # Base simples: times mais fortes têm chance um pouco maior de marcar.
    base = random.random()
    bonus = diferenca / 120
    valor = base + bonus

    if valor < 0.18:
        return 0
    if valor < 0.42:
        return 1
    if valor < 0.68:
        return 2
    if valor < 0.86:
        return 3
    if valor < 0.96:
        return 4
    return 5


def simular_placar(time_1: str, time_2: str) -> Tuple[int, int]:
    forca_1 = forca_da_selecao(time_1)
    forca_2 = forca_da_selecao(time_2)
    return simular_gols(time_1, forca_2), simular_gols(time_2, forca_1)


def registrar_resultado(tabela: TabelaGrupo, resultado: Resultado) -> None:
    time_1 = resultado.time_1
    time_2 = resultado.time_2
    gols_1 = resultado.gols_1
    gols_2 = resultado.gols_2

    tabela[time_1]["j"] += 1
    tabela[time_2]["j"] += 1

    tabela[time_1]["gp"] += gols_1
    tabela[time_1]["gc"] += gols_2
    tabela[time_2]["gp"] += gols_2
    tabela[time_2]["gc"] += gols_1

    tabela[time_1]["sg"] = tabela[time_1]["gp"] - tabela[time_1]["gc"]
    tabela[time_2]["sg"] = tabela[time_2]["gp"] - tabela[time_2]["gc"]

    if gols_1 > gols_2:
        tabela[time_1]["pts"] += 3
        tabela[time_1]["v"] += 1
        tabela[time_2]["d"] += 1
    elif gols_2 > gols_1:
        tabela[time_2]["pts"] += 3
        tabela[time_2]["v"] += 1
        tabela[time_1]["d"] += 1
    else:
        tabela[time_1]["pts"] += 1
        tabela[time_2]["pts"] += 1
        tabela[time_1]["e"] += 1
        tabela[time_2]["e"] += 1


# =========================================================
# COMPONENTES VISUAIS
# =========================================================

class Botao:
    def __init__(self, rect: pygame.Rect, rotulo: str, acao: Callable[[], None],
                 cor=BRANCO, cor_hover=AMARELO, cor_texto=PRETO):
        self.rect = rect
        self.rotulo = rotulo
        self.acao = acao
        self.cor = cor
        self.cor_hover = cor_hover
        self.cor_texto = cor_texto

    def desenhar(self, tela: pygame.Surface) -> None:
        mouse = pygame.mouse.get_pos()
        cor_base = self.cor_hover if self.rect.collidepoint(mouse) else self.cor
        pygame.draw.rect(tela, cor_base, self.rect, border_radius=14)
        pygame.draw.rect(tela, PRETO, self.rect, width=2, border_radius=14)
        texto(tela, self.rotulo, 22, self.rect.centerx, self.rect.centery,
              self.cor_texto, centro=True, negrito=True)

    def clicou(self, posicao: Tuple[int, int]) -> bool:
        return self.rect.collidepoint(posicao)


# =========================================================
# CLASSE PRINCIPAL
# =========================================================

class SimuladorCopa2026:
    def __init__(self, tela: pygame.Surface):
        self.tela = tela
        self.largura, self.altura = tela.get_size()
        self.estado = "menu"
        self.botoes: List[Botao] = []

        # Dados da Copa
        self.grupos: Dict[str, List[str]] = {}
        self.tabelas: Dict[str, TabelaGrupo] = {}
        self.partidas_grupos: List[PartidaGrupo] = []
        self.indice_partida_grupo = 0
        self.resultado_atual: Optional[Resultado] = None
        self.classificados_por_grupo: Dict[str, List[str]] = {}
        self.historico: List[str] = []

        # Mata-mata
        self.fase_mata_mata = ""
        self.partidas_mata_mata: List[PartidaMataMata] = []
        self.indice_mata_mata = 0
        self.vencedores_fase: List[str] = []
        self.campeao: Optional[str] = None

        # Quiz
        self.indice_pergunta = 0
        self.pontos_quiz = 0
        self.resposta_escolhida: Optional[int] = None
        self.quiz_respondido = False

    # -----------------------------------------------------
    # CONTROLE DE JANELA
    # -----------------------------------------------------

    def atualizar_tamanho(self, tela: pygame.Surface) -> None:
        self.tela = tela
        self.largura, self.altura = tela.get_size()

    # -----------------------------------------------------
    # BASE VISUAL
    # -----------------------------------------------------

    def fundo(self) -> None:
        self.tela.fill(AZUL_ESCURO)

        # Formas decorativas
        pygame.draw.circle(self.tela, AZUL_MEDIO, (80, 90), 180)
        pygame.draw.circle(self.tela, VERDE, (self.largura - 110, self.altura - 80), 230)
        pygame.draw.circle(self.tela, AMARELO, (self.largura - 80, 80), 85)

        margem = 42
        painel = pygame.Rect(margem, margem, self.largura - margem * 2, self.altura - margem * 2)
        pygame.draw.rect(self.tela, CARD, painel, border_radius=26)
        pygame.draw.rect(self.tela, AZUL_CLARO, painel, width=3, border_radius=26)

    def cabecalho(self, titulo: str, subtitulo: str = "") -> None:
        texto(self.tela, titulo, 40, self.largura // 2, 82, AMARELO, centro=True, negrito=True)
        if subtitulo:
            texto(self.tela, subtitulo, 22, self.largura // 2, 124, CINZA, centro=True)

    def rodape(self) -> None:
        texto(self.tela, "F11: tela cheia | ESC: voltar/sair | Projeto Python - Copa do Mundo 2026",
              18, self.largura // 2, self.altura - 68, CINZA, centro=True)

    def adicionar_botao(self, x: int, y: int, w: int, h: int, rotulo: str,
                       acao: Callable[[], None], cor=BRANCO, cor_hover=AMARELO) -> None:
        botao = Botao(pygame.Rect(x, y, w, h), rotulo, acao, cor=cor, cor_hover=cor_hover)
        self.botoes.append(botao)
        botao.desenhar(self.tela)

    def botao_central(self, y: int, rotulo: str, acao: Callable[[], None],
                     largura: int = 330, cor=BRANCO) -> None:
        self.adicionar_botao(self.largura // 2 - largura // 2, y, largura, 56, rotulo, acao, cor=cor)

    def voltar_menu(self) -> None:
        self.estado = "menu"

    def sair(self) -> None:
        pygame.quit()
        sys.exit()

    def esc(self) -> None:
        if self.estado == "menu":
            self.sair()
        else:
            self.estado = "menu"

    # -----------------------------------------------------
    # MENU
    # -----------------------------------------------------

    def desenhar_menu(self) -> None:
        self.fundo()
        self.cabecalho("SIMULADOR DA COPA DO MUNDO 2026", "Mini sistema em Python com simulação e quiz")

        centro = self.largura // 2
        y = 190
        espaco = 68
        largura = 360

        self.adicionar_botao(centro - largura // 2, y, largura, 56, "Iniciar Mini Copa 2026", self.iniciar_copa)
        self.adicionar_botao(centro - largura // 2, y + espaco, largura, 56, "Ver Seleções", self.ir_selecoes)
        self.adicionar_botao(centro - largura // 2, y + espaco * 2, largura, 56, "Ver Regras", self.ir_regras)
        self.adicionar_botao(centro - largura // 2, y + espaco * 3, largura, 56, "Quiz da Copa", self.iniciar_quiz)
        self.adicionar_botao(centro - largura // 2, y + espaco * 4, largura, 56, "Sair", self.sair, cor=VERMELHO, cor_hover=LARANJA)

        texto(self.tela, "Melhorias: 16 seleções, 4 grupos, quartas de final, histórico e sistema de força das equipes.",
              19, centro, self.altura - 110, BRANCO, centro=True)
        self.rodape()

    def ir_selecoes(self) -> None:
        self.estado = "selecoes"

    def desenhar_selecoes(self) -> None:
        self.fundo()
        self.cabecalho("SELEÇÕES DA SIMULAÇÃO", "Times usados no mini torneio")

        colunas = 2
        largura_coluna = 390
        inicio_x = self.largura // 2 - largura_coluna
        inicio_y = 165
        espaco_y = 42

        for i, selecao in enumerate(SELECOES, start=1):
            coluna = 0 if i <= 8 else 1
            linha = (i - 1) % 8
            x = inicio_x + coluna * largura_coluna
            y = inicio_y + linha * espaco_y
            nome = selecao["nome"]
            forca = selecao["forca"]
            texto(self.tela, f"{i:02d}. {nome:<16}  Força: {forca}", 24, x, y, BRANCO)

        self.botao_central(self.altura - 130, "Voltar ao Menu", self.voltar_menu)
        self.rodape()

    def ir_regras(self) -> None:
        self.estado = "regras"

    def desenhar_regras(self) -> None:
        self.fundo()
        self.cabecalho("REGRAS DO MINI SISTEMA", "Funcionamento da Copa dentro do projeto")

        regras = [
            "A Mini Copa 2026 possui 16 seleções divididas em 4 grupos.",
            "Cada grupo tem 4 seleções e todos jogam contra todos dentro do grupo.",
            "Vitória vale 3 pontos, empate vale 1 ponto e derrota vale 0 ponto.",
            "A classificação usa pontos, saldo de gols, gols marcados e ordem alfabética como desempate.",
            "Os 2 melhores de cada grupo avançam para as quartas de final.",
            "O mata-mata tem quartas, semifinais e final.",
            "Se uma partida eliminatória terminar empatada, a decisão vai para os pênaltis.",
            "O projeto também possui um quiz de conhecimentos gerais sobre Copa do Mundo.",
        ]

        y = 165
        for regra in regras:
            pygame.draw.circle(self.tela, AMARELO, (135, y + 12), 5)
            texto_quebrado(self.tela, regra, 24, 155, y, self.largura - 300, BRANCO)
            y += 48

        self.botao_central(self.altura - 120, "Voltar ao Menu", self.voltar_menu)
        self.rodape()

    # -----------------------------------------------------
    # QUIZ
    # -----------------------------------------------------

    def iniciar_quiz(self) -> None:
        self.indice_pergunta = 0
        self.pontos_quiz = 0
        self.resposta_escolhida = None
        self.quiz_respondido = False
        self.estado = "quiz"

    def responder_quiz(self, indice: int) -> None:
        if self.quiz_respondido:
            return

        self.resposta_escolhida = indice
        self.quiz_respondido = True
        pergunta = PERGUNTAS_QUIZ[self.indice_pergunta]
        if indice == pergunta["resposta"]:
            self.pontos_quiz += 1

    def proxima_pergunta(self) -> None:
        if not self.quiz_respondido:
            return
        self.indice_pergunta += 1
        self.resposta_escolhida = None
        self.quiz_respondido = False

    def desenhar_quiz(self) -> None:
        self.fundo()
        self.cabecalho("QUIZ DA COPA DO MUNDO", "Teste seus conhecimentos antes da final")

        total = len(PERGUNTAS_QUIZ)
        if self.indice_pergunta >= total:
            self.desenhar_resultado_quiz()
            return

        pergunta = PERGUNTAS_QUIZ[self.indice_pergunta]
        correto = pergunta["resposta"]

        texto(self.tela, f"Pergunta {self.indice_pergunta + 1} de {total}",
              24, self.largura // 2, 158, AMARELO, centro=True, negrito=True)
        texto_quebrado(self.tela, pergunta["pergunta"], 29, 135, 205, self.largura - 270, BRANCO, negrito=True)

        largura = min(760, self.largura - 260)
        x = self.largura // 2 - largura // 2
        y = 325

        for i, opcao in enumerate(pergunta["opcoes"]):
            cor = BRANCO
            hover = AMARELO
            if self.quiz_respondido:
                if i == correto:
                    cor = VERDE_CLARO
                    hover = VERDE_CLARO
                elif i == self.resposta_escolhida:
                    cor = VERMELHO
                    hover = VERMELHO

            self.adicionar_botao(x, y + i * 62, largura, 50, f"{i + 1}. {opcao}",
                                 lambda idx=i: self.responder_quiz(idx), cor=cor, cor_hover=hover)

        texto(self.tela, f"Pontuação: {self.pontos_quiz}", 23, self.largura - 260, self.altura - 100, BRANCO)
        self.adicionar_botao(85, self.altura - 120, 250, 52, "Voltar ao Menu", self.voltar_menu)

        if self.quiz_respondido:
            mensagem = "Resposta correta!" if self.resposta_escolhida == correto else "Resposta incorreta. A correta está em verde."
            cor_msg = VERDE_CLARO if self.resposta_escolhida == correto else VERMELHO
            texto(self.tela, mensagem, 22, self.largura // 2, self.altura - 132, cor_msg, centro=True, negrito=True)
            self.adicionar_botao(self.largura // 2 - 130, self.altura - 100, 260, 52, "Próxima", self.proxima_pergunta, cor=AMARELO)

        self.rodape()

    def desenhar_resultado_quiz(self) -> None:
        total = len(PERGUNTAS_QUIZ)
        texto(self.tela, "RESULTADO DO QUIZ", 36, self.largura // 2, 200, AMARELO, centro=True, negrito=True)
        texto(self.tela, f"Você acertou {self.pontos_quiz} de {total} perguntas.",
              34, self.largura // 2, 270, BRANCO, centro=True, negrito=True)

        percentual = self.pontos_quiz / total
        if percentual >= 0.8:
            mensagem = "Excelente! Você está pronto para narrar a final."
        elif percentual >= 0.5:
            mensagem = "Bom resultado! Você conhece bastante sobre Copa."
        else:
            mensagem = "Boa tentativa! Vale revisar um pouco mais a história da Copa."

        texto_quebrado(self.tela, mensagem, 27, self.largura // 2 - 360, 330, 720, AMARELO, negrito=True)
        self.adicionar_botao(self.largura // 2 - 320, 440, 280, 56, "Jogar Quiz de Novo", self.iniciar_quiz)
        self.adicionar_botao(self.largura // 2 + 40, 440, 280, 56, "Voltar ao Menu", self.voltar_menu)
        self.rodape()

    # -----------------------------------------------------
    # COPA - INÍCIO E FASE DE GRUPOS
    # -----------------------------------------------------

    def iniciar_copa(self) -> None:
        nomes = [s["nome"] for s in SELECOES]
        random.shuffle(nomes)

        self.grupos = {
            "Grupo A": nomes[0:4],
            "Grupo B": nomes[4:8],
            "Grupo C": nomes[8:12],
            "Grupo D": nomes[12:16],
        }
        self.tabelas = {grupo: criar_tabela(times) for grupo, times in self.grupos.items()}
        self.partidas_grupos = []
        for grupo, times in self.grupos.items():
            self.partidas_grupos.extend(gerar_partidas_grupo(grupo, times))

        self.indice_partida_grupo = 0
        self.resultado_atual = None
        self.classificados_por_grupo = {}
        self.historico = ["A Mini Copa do Mundo 2026 começou!"]
        self.partidas_mata_mata = []
        self.indice_mata_mata = 0
        self.vencedores_fase = []
        self.campeao = None
        self.estado = "intro_copa"

    def desenhar_intro_copa(self) -> None:
        self.fundo()
        self.cabecalho("SORTEIO DOS GRUPOS", "A Mini Copa 2026 está pronta para começar")

        x_inicial = 100
        y_inicial = 170
        largura_card = (self.largura - 250) // 2
        altura_card = 185
        grupos = list(self.grupos.items())

        for idx, (grupo, times) in enumerate(grupos):
            coluna = idx % 2
            linha = idx // 2
            x = x_inicial + coluna * (largura_card + 50)
            y = y_inicial + linha * (altura_card + 25)
            card = pygame.Rect(x, y, largura_card, altura_card)
            pygame.draw.rect(self.tela, CARD_2, card, border_radius=18)
            pygame.draw.rect(self.tela, AZUL_CLARO, card, width=2, border_radius=18)
            texto(self.tela, grupo, 28, x + 24, y + 18, AMARELO, negrito=True)
            for i, time_nome in enumerate(times):
                texto(self.tela, f"- {time_nome}", 23, x + 32, y + 62 + i * 29, BRANCO)

        self.botao_central(self.altura - 120, "Começar Fase de Grupos", self.ir_partida_grupo, largura=360)
        self.rodape()

    def ir_partida_grupo(self) -> None:
        if self.indice_partida_grupo >= len(self.partidas_grupos):
            self.calcular_classificados()
            self.estado = "classificados"
        else:
            self.resultado_atual = None
            self.estado = "partida_grupo"

    def partida_grupo_atual(self) -> PartidaGrupo:
        return self.partidas_grupos[self.indice_partida_grupo]

    def desenhar_partida_grupo(self) -> None:
        self.fundo()
        grupo, time_1, time_2 = self.partida_grupo_atual()
        total = len(self.partidas_grupos)

        self.cabecalho(f"{grupo} - PARTIDA {self.indice_partida_grupo + 1}/{total}", "Fase de grupos")
        texto(self.tela, "Próximo jogo", 28, self.largura // 2, 215, CINZA, centro=True)
        texto(self.tela, f"{time_1}  x  {time_2}", 50, self.largura // 2, 285, AMARELO, centro=True, negrito=True)

        self.desenhar_tabela(grupo, 120, 380, largura=460)
        self.desenhar_historico(self.largura - 500, 380, 390, 190)

        self.botao_central(self.altura - 125, "Simular Partida", self.simular_partida_grupo, largura=320)
        self.rodape()

    def simular_partida_grupo(self) -> None:
        grupo, time_1, time_2 = self.partida_grupo_atual()
        gols_1, gols_2 = simular_placar(time_1, time_2)
        resultado = Resultado(time_1, time_2, gols_1, gols_2)
        registrar_resultado(self.tabelas[grupo], resultado)
        self.resultado_atual = resultado

        if gols_1 > gols_2:
            resumo = f"{grupo}: {time_1} venceu {time_2} por {gols_1} x {gols_2}."
        elif gols_2 > gols_1:
            resumo = f"{grupo}: {time_2} venceu {time_1} por {gols_2} x {gols_1}."
        else:
            resumo = f"{grupo}: {time_1} e {time_2} empataram em {gols_1} x {gols_2}."
        self.historico.append(resumo)
        self.estado = "resultado_grupo"

    def desenhar_resultado_grupo(self) -> None:
        self.fundo()
        grupo, _, _ = self.partida_grupo_atual()
        r = self.resultado_atual
        assert r is not None

        self.cabecalho(f"RESULTADO - {grupo}", "Tabela atualizada automaticamente")
        texto(self.tela, f"{r.time_1} {r.gols_1} x {r.gols_2} {r.time_2}",
              48, self.largura // 2, 210, BRANCO, centro=True, negrito=True)

        if r.gols_1 > r.gols_2:
            msg = f"Vencedor: {r.time_1}"
        elif r.gols_2 > r.gols_1:
            msg = f"Vencedor: {r.time_2}"
        else:
            msg = "Empate na fase de grupos"
        texto(self.tela, msg, 28, self.largura // 2, 265, AMARELO, centro=True, negrito=True)

        self.desenhar_tabela(grupo, 110, 340, largura=500)
        self.desenhar_historico(self.largura - 510, 340, 400, 230)

        texto_botao = "Ver Classificados" if self.indice_partida_grupo == len(self.partidas_grupos) - 1 else "Próxima Partida"
        self.botao_central(self.altura - 120, texto_botao, self.avancar_partida_grupo, largura=330)
        self.rodape()

    def avancar_partida_grupo(self) -> None:
        self.indice_partida_grupo += 1
        self.ir_partida_grupo()

    def calcular_classificados(self) -> None:
        self.classificados_por_grupo = {}
        for grupo, tabela in self.tabelas.items():
            ordenados = ordenar_tabela(tabela)
            self.classificados_por_grupo[grupo] = [ordenados[0][0], ordenados[1][0]]

    def desenhar_classificados(self) -> None:
        self.fundo()
        self.cabecalho("CLASSIFICADOS PARA O MATA-MATA", "Os dois melhores de cada grupo avançam")

        grupos = list(self.grupos.keys())
        x1 = 95
        y1 = 160
        largura = (self.largura - 230) // 2

        for idx, grupo in enumerate(grupos):
            coluna = idx % 2
            linha = idx // 2
            x = x1 + coluna * (largura + 40)
            y = y1 + linha * 205
            self.desenhar_tabela(grupo, x, y, largura=largura, compacto=True)
            classificados = self.classificados_por_grupo[grupo]
            texto(self.tela, f"Classificados: {classificados[0]} e {classificados[1]}",
                  20, x + 18, y + 162, AMARELO, negrito=True)

        self.botao_central(self.altura - 95, "Montar Quartas de Final", self.iniciar_quartas, largura=360)
        self.rodape()

    # -----------------------------------------------------
    # DESENHOS DE TABELA E HISTÓRICO
    # -----------------------------------------------------

    def desenhar_tabela(self, grupo: str, x: int, y: int, largura: int = 480, compacto: bool = False) -> None:
        tabela = self.tabelas[grupo]
        ordenados = ordenar_tabela(tabela)
        altura = 178 if compacto else 205
        rect = pygame.Rect(x, y, largura, altura)
        pygame.draw.rect(self.tela, CARD_2, rect, border_radius=16)
        pygame.draw.rect(self.tela, AZUL_CLARO, rect, width=2, border_radius=16)

        texto(self.tela, grupo, 24, x + 16, y + 14, AMARELO, negrito=True)
        cabecalho = "Pos  Seleção           Pts  J  V  E  D  SG"
        texto(self.tela, cabecalho, 18, x + 16, y + 48, CINZA, negrito=True)

        linha_y = y + 75
        for pos, (nome, dados) in enumerate(ordenados, start=1):
            linha = (
                f"{pos:<4} {nome:<16.16} "
                f"{dados['pts']:<4} {dados['j']:<2} {dados['v']:<2} {dados['e']:<2} {dados['d']:<2} {dados['sg']:<3}"
            )
            cor = VERDE_CLARO if pos <= 2 else BRANCO
            texto(self.tela, linha, 18, x + 16, linha_y, cor)
            linha_y += 28 if compacto else 30

    def desenhar_historico(self, x: int, y: int, largura: int, altura: int) -> None:
        rect = pygame.Rect(x, y, largura, altura)
        pygame.draw.rect(self.tela, CARD_2, rect, border_radius=16)
        pygame.draw.rect(self.tela, AZUL_CLARO, rect, width=2, border_radius=16)
        texto(self.tela, "Histórico recente", 23, x + 18, y + 15, AMARELO, negrito=True)

        itens = self.historico[-5:]
        linha_y = y + 55
        for item in itens:
            linha_y = texto_quebrado(self.tela, item, 18, x + 18, linha_y, largura - 36, BRANCO, espacamento=4)
            linha_y += 6

    # -----------------------------------------------------
    # MATA-MATA
    # -----------------------------------------------------

    def iniciar_quartas(self) -> None:
        a1, a2 = self.classificados_por_grupo["Grupo A"]
        b1, b2 = self.classificados_por_grupo["Grupo B"]
        c1, c2 = self.classificados_por_grupo["Grupo C"]
        d1, d2 = self.classificados_por_grupo["Grupo D"]

        self.fase_mata_mata = "Quartas de Final"
        self.partidas_mata_mata = [
            ("Quartas 1", a1, b2),
            ("Quartas 2", b1, a2),
            ("Quartas 3", c1, d2),
            ("Quartas 4", d1, c2),
        ]
        self.indice_mata_mata = 0
        self.vencedores_fase = []
        self.resultado_atual = None
        self.estado = "intro_mata_mata"

    def desenhar_intro_mata_mata(self) -> None:
        self.fundo()
        self.cabecalho(self.fase_mata_mata.upper(), "Confrontos eliminatórios")

        y = 190
        for fase, time_1, time_2 in self.partidas_mata_mata:
            rect = pygame.Rect(self.largura // 2 - 390, y - 12, 780, 52)
            pygame.draw.rect(self.tela, CARD_2, rect, border_radius=14)
            pygame.draw.rect(self.tela, AZUL_CLARO, rect, width=1, border_radius=14)
            texto(self.tela, f"{fase}: {time_1}  x  {time_2}", 26,
                  self.largura // 2, y + 12, BRANCO, centro=True, negrito=True)
            y += 68

        self.botao_central(self.altura - 120, "Começar Mata-Mata", self.ir_partida_mata_mata, largura=330)
        self.rodape()

    def ir_partida_mata_mata(self) -> None:
        self.resultado_atual = None
        self.estado = "partida_mata_mata"

    def partida_mata_mata_atual(self) -> PartidaMataMata:
        return self.partidas_mata_mata[self.indice_mata_mata]

    def desenhar_partida_mata_mata(self) -> None:
        self.fundo()
        fase, time_1, time_2 = self.partida_mata_mata_atual()
        self.cabecalho(fase.upper(), self.fase_mata_mata)

        texto(self.tela, "Jogo decisivo", 28, self.largura // 2, 220, CINZA, centro=True)
        texto(self.tela, f"{time_1}  x  {time_2}", 52, self.largura // 2, 300, AMARELO, centro=True, negrito=True)
        texto(self.tela, "Em caso de empate, a partida será decidida nos pênaltis.",
              23, self.largura // 2, 365, BRANCO, centro=True)

        self.desenhar_historico(self.largura // 2 - 260, 415, 520, 120)
        self.botao_central(self.altura - 115, "Simular Jogo", self.simular_partida_mata_mata, largura=300)
        self.rodape()

    def simular_penaltis(self, time_1: str, time_2: str) -> Tuple[int, int, str]:
        p1 = random.randint(3, 5)
        p2 = random.randint(3, 5)
        while p1 == p2:
            p1 = random.randint(3, 5)
            p2 = random.randint(3, 5)
        vencedor = time_1 if p1 > p2 else time_2
        return p1, p2, vencedor

    def simular_partida_mata_mata(self) -> None:
        fase, time_1, time_2 = self.partida_mata_mata_atual()
        gols_1, gols_2 = simular_placar(time_1, time_2)
        penaltis_1 = None
        penaltis_2 = None

        if gols_1 > gols_2:
            vencedor = time_1
        elif gols_2 > gols_1:
            vencedor = time_2
        else:
            penaltis_1, penaltis_2, vencedor = self.simular_penaltis(time_1, time_2)

        self.resultado_atual = Resultado(
            time_1=time_1,
            time_2=time_2,
            gols_1=gols_1,
            gols_2=gols_2,
            vencedor=vencedor,
            penaltis_1=penaltis_1,
            penaltis_2=penaltis_2,
        )
        self.vencedores_fase.append(vencedor)

        if penaltis_1 is None:
            self.historico.append(f"{fase}: {vencedor} avançou após {gols_1} x {gols_2}.")
        else:
            self.historico.append(f"{fase}: {vencedor} avançou nos pênaltis ({penaltis_1} x {penaltis_2}).")

        self.estado = "resultado_mata_mata"

    def desenhar_resultado_mata_mata(self) -> None:
        self.fundo()
        fase, _, _ = self.partida_mata_mata_atual()
        r = self.resultado_atual
        assert r is not None

        self.cabecalho(f"RESULTADO - {fase.upper()}", self.fase_mata_mata)
        texto(self.tela, f"{r.time_1} {r.gols_1} x {r.gols_2} {r.time_2}",
              52, self.largura // 2, 220, BRANCO, centro=True, negrito=True)

        y = 305
        if r.penaltis_1 is not None and r.penaltis_2 is not None:
            texto(self.tela, "Empate no tempo normal. Decisão nos pênaltis:",
                  25, self.largura // 2, y, CINZA, centro=True)
            y += 55
            texto(self.tela, f"{r.time_1} {r.penaltis_1} x {r.penaltis_2} {r.time_2}",
                  40, self.largura // 2, y, AMARELO, centro=True, negrito=True)
            y += 65

        texto(self.tela, f"Classificado: {r.vencedor}", 34, self.largura // 2, y,
              AMARELO, centro=True, negrito=True)

        self.desenhar_historico(self.largura // 2 - 280, y + 55, 560, 115)

        if self.fase_mata_mata == "Final":
            rotulo = "Ver Campeão"
        elif self.indice_mata_mata == len(self.partidas_mata_mata) - 1:
            rotulo = "Próxima Fase"
        else:
            rotulo = "Próximo Jogo"

        self.botao_central(self.altura - 110, rotulo, self.avancar_mata_mata, largura=310)
        self.rodape()

    def avancar_mata_mata(self) -> None:
        if self.fase_mata_mata == "Final":
            self.campeao = self.vencedores_fase[0]
            self.estado = "campeao"
            return

        self.indice_mata_mata += 1
        if self.indice_mata_mata < len(self.partidas_mata_mata):
            self.estado = "partida_mata_mata"
            return

        # Fase terminou. Monta a próxima fase.
        vencedores = self.vencedores_fase[:]
        self.vencedores_fase = []
        self.indice_mata_mata = 0

        if self.fase_mata_mata == "Quartas de Final":
            self.fase_mata_mata = "Semifinais"
            self.partidas_mata_mata = [
                ("Semifinal 1", vencedores[0], vencedores[1]),
                ("Semifinal 2", vencedores[2], vencedores[3]),
            ]
            self.estado = "intro_mata_mata"
        elif self.fase_mata_mata == "Semifinais":
            self.fase_mata_mata = "Final"
            self.partidas_mata_mata = [
                ("Grande Final", vencedores[0], vencedores[1]),
            ]
            self.estado = "intro_mata_mata"

    def desenhar_campeao(self) -> None:
        self.fundo()
        self.cabecalho("FIM DE COPA", "A Mini Copa do Mundo 2026 terminou")

        texto(self.tela, "CAMPEÃO", 46, self.largura // 2, 220, AMARELO, centro=True, negrito=True)
        texto(self.tela, (self.campeao or "").upper(), 70, self.largura // 2, 315,
              BRANCO, centro=True, negrito=True)
        texto(self.tela, "Parabéns ao campeão da simulação!", 27, self.largura // 2, 395,
              VERDE_CLARO, centro=True, negrito=True)

        self.desenhar_historico(self.largura // 2 - 330, 445, 660, 110)
        self.adicionar_botao(self.largura // 2 - 330, self.altura - 115, 280, 56, "Nova Copa", self.iniciar_copa)
        self.adicionar_botao(self.largura // 2 + 50, self.altura - 115, 280, 56, "Menu Principal", self.voltar_menu)
        self.rodape()

    # -----------------------------------------------------
    # DESENHO GERAL
    # -----------------------------------------------------

    def desenhar(self) -> None:
        self.botoes = []

        if self.estado == "menu":
            self.desenhar_menu()
        elif self.estado == "selecoes":
            self.desenhar_selecoes()
        elif self.estado == "regras":
            self.desenhar_regras()
        elif self.estado == "quiz":
            self.desenhar_quiz()
        elif self.estado == "intro_copa":
            self.desenhar_intro_copa()
        elif self.estado == "partida_grupo":
            self.desenhar_partida_grupo()
        elif self.estado == "resultado_grupo":
            self.desenhar_resultado_grupo()
        elif self.estado == "classificados":
            self.desenhar_classificados()
        elif self.estado == "intro_mata_mata":
            self.desenhar_intro_mata_mata()
        elif self.estado == "partida_mata_mata":
            self.desenhar_partida_mata_mata()
        elif self.estado == "resultado_mata_mata":
            self.desenhar_resultado_mata_mata()
        elif self.estado == "campeao":
            self.desenhar_campeao()
        else:
            self.estado = "menu"
            self.desenhar_menu()


# =========================================================
# EXECUÇÃO
# =========================================================

def criar_tela(tela_cheia: bool) -> pygame.Surface:
    if tela_cheia:
        return pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    return pygame.display.set_mode((LARGURA_INICIAL, ALTURA_INICIAL), pygame.RESIZABLE)


def main() -> None:
    pygame.init()
    pygame.display.set_caption(TITULO_JANELA)

    tela_cheia = False
    tela = criar_tela(tela_cheia)
    relogio = pygame.time.Clock()
    jogo = SimuladorCopa2026(tela)

    while True:
        jogo.desenhar()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jogo.sair()

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    jogo.esc()

                elif evento.key == pygame.K_F11:
                    tela_cheia = not tela_cheia
                    tela = criar_tela(tela_cheia)
                    jogo.atualizar_tamanho(tela)

            elif evento.type == pygame.VIDEORESIZE and not tela_cheia:
                tela = pygame.display.set_mode((evento.w, evento.h), pygame.RESIZABLE)
                jogo.atualizar_tamanho(tela)

            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                posicao = pygame.mouse.get_pos()
                for botao in jogo.botoes:
                    if botao.clicou(posicao):
                        botao.acao()
                        break

        pygame.display.flip()
        relogio.tick(FPS)


if __name__ == "__main__":
    main()
