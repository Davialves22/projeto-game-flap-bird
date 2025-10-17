# 🐦 Flappy Bird Clone em Python

Clone do clássico *Flappy Bird*, feito em Python com **Pygame**. Controle seu pássaro, evite os canos e tente bater sua própria pontuação!

![Tela Principal](docs/tela_principal.png)

> Tela principal do jogo, com o pássaro pronto para voar.

![Game Over](docs/tela_game_over.png)

> Tela de Game Over, com opção de **Jogar Novamente** ou **Sair**.

---

## 🎮 Funcionalidades

* Controle do pássaro com **Espaço**
* Obstáculos (canos) gerados aleatoriamente
* Pontuação exibida na tela
* Tela de **Game Over** com botões:

  * Jogar Novamente
  * Sair do jogo
* Animação do pássaro e do cenário

---

## 🖥️ Pré-requisitos

* Python 3.8 ou superior
* [Pygame](https://www.pygame.org/)

Instale o Pygame:

```bash
pip install pygame
```

---

## 🚀 Como Jogar

1. Clone ou baixe o projeto.
2. Garanta que a pasta `imgs/` esteja no mesmo diretório do script, com estas imagens:

```
imgs/
├─ bird1.png
├─ bird2.png
├─ bird3.png
├─ pipe.png
├─ base.png
└─ bg.png
```

3. Execute o arquivo principal:

```bash
python main.py
```

4. Pressione **Espaço** para pular.
5. Evite colidir com canos ou chão.
6. Na tela de Game Over, escolha entre **Jogar Novamente** ou **Sair**.

---

## 📂 Estrutura de Pastas

```
project_root/
│
├─ imgs/            # Imagens do jogo
│   ├─ bird1.png
│   ├─ bird2.png
│   ├─ bird3.png
│   ├─ pipe.png
│   ├─ base.png
│   └─ bg.png
│
├─ main.py          # Código principal
├─ README.md        # Este arquivo
└─ docs/            # Capturas de tela para o README
    ├─ tela_principal.png
    └─ tela_game_over.png
```

---

## 🛠️ Personalizações

* **Velocidade do pássaro e canos:** ajuste `VELOCIDADE` e `VELOCIDADE_ROTACAO`
* **Distância entre canos:** altere `DISTANCIA` na classe `Cano`
* **Substituir sprites e fundo:** troque os arquivos da pasta `imgs/`

---

## 📜 Licença

Este projeto é **open-source**, livre para estudo, modificação e compartilhamento.

---
