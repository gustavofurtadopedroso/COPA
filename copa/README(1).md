# Simulador da Copa do Mundo 2026

Mini sistema desenvolvido em **Python** com o tema **Copa do Mundo 2026**.

O projeto simula uma mini competição de futebol com fase de grupos, classificação automática, mata-mata, final, campeão e um quiz temático sobre Copa do Mundo.

---

## Objetivo do projeto

Este projeto foi desenvolvido para uma atividade acadêmica em que os alunos devem finalizar, apresentar e publicar no GitHub um mini sistema em Python com tema relacionado à Copa do Mundo 2026.

A ideia do sistema é permitir que o usuário acompanhe uma simulação interativa da Copa, passando partida por partida, visualizando resultados, classificação e campeão final.

---

## Funcionalidades

- Menu principal com navegação por botões;
- Simulação de uma Mini Copa do Mundo 2026;
- 16 seleções participantes;
- 4 grupos com 4 seleções cada;
- Fase de grupos com todos contra todos;
- Tabela de classificação automática;
- Critérios de classificação por pontos, saldo de gols e gols marcados;
- Quartas de final, semifinais e final;
- Decisão por pênaltis em jogos eliminatórios empatados;
- Histórico recente dos jogos;
- Sistema simples de força das seleções;
- Quiz temático sobre Copa do Mundo;
- Interface gráfica feita com Pygame;
- Suporte a tela cheia com a tecla `F11`;
- Saída/voltar com a tecla `ESC`.

---

## Tecnologias utilizadas

- Python 3
- Pygame
- Random
- Dataclasses

---

## Estrutura do projeto

```text
simulador-copa-2026/
│
├── simulador_copa_2026.py
├── requirements.txt
└── README.md
```

---

## Como executar o projeto

### 1. Instale o Python

Baixe e instale o Python pelo site oficial:

```text
https://www.python.org/downloads/
```

Durante a instalação, marque a opção:

```text
Add Python to PATH
```

---

### 2. Instale as dependências

No terminal, dentro da pasta do projeto, execute:

```bash
pip install -r requirements.txt
```

Ou instale o Pygame diretamente:

```bash
pip install pygame
```

---

### 3. Execute o jogo

No terminal, dentro da pasta do projeto, execute:

```bash
python simulador_copa_2026.py
```

Caso seu computador use `python3`, execute:

```bash
python3 simulador_copa_2026.py
```

---

## Controles

| Tecla / Ação | Função |
|---|---|
| Mouse | Clicar nos botões do menu e do jogo |
| F11 | Alternar entre janela e tela cheia |
| ESC | Voltar ao menu ou sair do jogo |

---

## Como o sistema funciona

Ao iniciar o jogo, o usuário pode escolher entre:

1. Iniciar a Mini Copa 2026;
2. Ver as seleções participantes;
3. Ver as regras;
4. Jogar o quiz da Copa;
5. Sair.

Na simulação da Copa, o sistema sorteia as seleções em 4 grupos. Em seguida, o usuário acompanha os jogos da fase de grupos, vê a classificação atualizada e avança para o mata-mata.

Os 2 melhores de cada grupo avançam para as quartas de final. Depois acontecem semifinais e final. Ao final, o sistema mostra o campeão da Mini Copa do Mundo 2026.

---

## Regras da Mini Copa 2026

- Vitória vale 3 pontos;
- Empate vale 1 ponto;
- Derrota vale 0 ponto;
- Os 2 melhores de cada grupo avançam;
- Em jogos eliminatórios, empate vai para os pênaltis;
- O vencedor da final é declarado campeão.

---

## Observação

As seleções e os grupos usados no projeto são parte de uma simulação fictícia. O objetivo do sistema é acadêmico e demonstrativo, não representar oficialmente os grupos reais da Copa do Mundo 2026.

---

## Sugestão para apresentação

Durante a apresentação, mostre:

1. O menu principal;
2. A tela de seleções;
3. As regras do sistema;
4. Uma simulação de algumas partidas;
5. A classificação dos grupos;
6. O mata-mata;
7. O campeão;
8. O quiz da Copa.

---

## Autor

Desenvolvido por **Gustavo Furtado Pedroso**.
