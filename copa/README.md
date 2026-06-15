# 🏆 Simulador da Copa

Projeto em Python com temática da Copa do Mundo. O programa permite simular uma mini competição entre 8 seleções, com fase de grupos, classificação, semifinais, final, campeão e uma versão gráfica feita com Pygame.

## 📌 Sobre o projeto

O **Simulador da Copa** foi desenvolvido como um projeto simples, interativo e bem organizado para praticar lógica de programação em Python. O projeto possui duas versões:

- `copa.py`: versão em terminal, feita em Python puro.
- `copa_pygame.py`: versão gráfica, feita com Pygame.

Na simulação, as seleções são divididas em dois grupos. Cada grupo possui 4 seleções, todos jogam contra todos, os dois melhores de cada grupo avançam para as semifinais e o vencedor da final se torna o campeão.

## 🚀 Funcionalidades

### Versão terminal — `copa.py`

- Menu principal interativo.
- Exibição das seleções participantes.
- Exibição das regras da competição.
- Sorteio automático dos grupos.
- Simulação da fase de grupos jogo por jogo.
- Tabela de classificação com pontos, jogos, vitórias, empates, derrotas, gols pró, gols contra e saldo de gols.
- Semifinais e final.
- Disputa de pênaltis em caso de empate no mata-mata.
- Modo manual para avançar jogo por jogo.
- Modo automático com avanço após alguns segundos.

### Versão gráfica — `copa_pygame.py`

- Interface visual com Pygame.
- Tela inicial com botões.
- Simulação da Copa de forma interativa.
- Visualização das seleções participantes.
- Tela de regras.
- Fase de grupos, classificação, semifinais, final e campeão.
- Quiz da Copa com perguntas gerais e ênfase no Brasil.
- Suporte a tela cheia.
- Suporte a redimensionamento da janela.

## 🛠️ Tecnologias utilizadas

- Python 3
- Biblioteca `random`
- Biblioteca `os`
- Biblioteca `time`
- Biblioteca `sys`
- Pygame

## 📁 Estrutura dos arquivos

```text
simulador-da-copa/
│
├── copa.py           # Versão em terminal
├── copa_pygame.py    # Versão gráfica com Pygame
└── README.md         # Documentação do projeto
```

## ✅ Pré-requisitos

Para executar a versão de terminal, é necessário ter apenas o Python instalado.

Para executar a versão gráfica, é necessário instalar também o Pygame.

Verifique se o Python está instalado:

```bash
python --version
```

ou:

```bash
python3 --version
```

## 📦 Instalação do Pygame

Para instalar o Pygame, use:

```bash
pip install pygame
```

Caso o comando `pip` não funcione, tente:

```bash
python -m pip install pygame
```

ou:

```bash
python3 -m pip install pygame
```

## ▶️ Como executar

### Executar a versão em terminal

```bash
python copa.py
```

ou:

```bash
python3 copa.py
```

### Executar a versão gráfica com Pygame

```bash
python copa_pygame.py
```

ou:

```bash
python3 copa_pygame.py
```

## 🎮 Controles

### Terminal

Na versão de terminal, o usuário escolhe as opções digitando números no menu.

Durante a simulação, no modo manual, digite `1` para avançar para a próxima etapa.

### Pygame

- Use o mouse para clicar nos botões.
- Pressione `F11` para alternar entre tela cheia e janela.
- Pressione `ESC` para sair do jogo.

## ⚽ Regras da competição

- A competição possui 8 seleções.
- As seleções são divididas em 2 grupos com 4 times cada.
- Na fase de grupos, todos jogam contra todos dentro do mesmo grupo.
- Vitória vale 3 pontos.
- Empate vale 1 ponto.
- Derrota vale 0 ponto.
- Os 2 melhores de cada grupo avançam para a semifinal.
- Em jogos eliminatórios, caso haja empate, a decisão vai para os pênaltis.
- O vencedor da final é declarado campeão.

## 🌍 Seleções participantes

- Brasil
- Argentina
- França
- Alemanha
- Espanha
- Inglaterra
- Portugal
- Uruguai

## 🧠 Quiz da Copa

A versão em Pygame possui uma área de quiz com perguntas sobre a Copa do Mundo, principalmente relacionadas ao Brasil.

O jogador responde às perguntas clicando nas alternativas e, ao final, recebe sua pontuação.

## 🧩 Possíveis melhorias futuras

- Adicionar nomes de jogadores.
- Criar níveis de dificuldade.
- Salvar histórico dos campeões.
- Adicionar sons e efeitos visuais.
- Criar uma tela de estatísticas completas.
- Permitir que o usuário escolha as seleções.
- Adicionar escudos ou bandeiras das seleções.
- Melhorar o sistema de quiz com feedback de resposta certa ou errada.

## 👨‍💻 Autor

Desenvolvido como projeto de estudo em Python.

## 📄 Licença

Este projeto é livre para fins de estudo, aprendizado e modificação.
