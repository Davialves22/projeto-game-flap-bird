# Importa a biblioteca principal do Pygame
import pygame
# Importa a biblioteca para interagir com o sistema operacional (usada para carregar imagens)
import os
# Importa a biblioteca para gerar números aleatórios (usada para a altura dos canos)
import random

# Define a largura da janela do jogo em pixels
TELA_LARGURA = 500
# Define a altura da janela do jogo em pixels
TELA_ALTURA = 800

# criando elementos do jogo
# Carrega e escala a imagem do cano (cano.png)
IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
# Carrega e escala a imagem do chão/base (base.png)
IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
# Carrega e escala a imagem de fundo (bg.png)
IMAGEM_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
# Carrega e escala as três imagens para a animação do pássaro (bird1, bird2, bird3)
IMAGEMS_PASSARO = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png')))
]

# Inicializa o módulo de fonte do Pygame
pygame.font.init()
# Define a fonte e o tamanho para exibir a pontuação na tela
FONTE_PONTOS = pygame.font.SysFont('arial', 50)


# classes para cada elemento
# Classe que representa o pássaro
class Passaro:
    # Atributo de classe: lista com as imagens de animação do pássaro
    IMGS = IMAGEMS_PASSARO

    # animações da rotação
    # Define o ângulo máximo de rotação do pássaro para cima
    ROTACAO_MAXIMA = 25
    # Define a velocidade de rotação do pássaro ao cair
    VELOCIDADE_ROTACAO = 20
    # Define o tempo de exibição de cada quadro da animação das asas
    TEMPO_ANIMACAO = 5

    # caracteristicas do passado
    # Construtor da classe: inicializa o pássaro em uma posição (x, y) e define estados iniciais
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0  # Rotação atual
        self.velocidade = 0  # Velocidade vertical
        self.altura = self.y  # Posição y de onde o pulo começou (para cálculo)
        self.tempo = 0  # Contador de tempo desde o último pulo
        self.contagem_imagem = 0  # Contador de tempo para a animação das asas
        self.imagem = self.IMGS[0]  # Imagem inicial do pássaro

    # função de pular
    # Define a velocidade inicial para o movimento de subida (pulo)
    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    # Move o pássaro verticalmente aplicando a gravidade
    def mover(self):
        # calcular o desclocamento
        # Incrementa o tempo desde o último pulo
        self.tempo += 1
        # Calcula o deslocamento vertical (simulação de gravidade e movimento parabólico)
        deslocamento = 1.5 * (self.tempo ** 2) + self.velocidade * self.tempo

        # restringir o deslocamento
        # Limita o deslocamento máximo para baixo
        if deslocamento > 16:
            deslocamento = 16
        # Se o deslocamento é para cima, aumenta ligeiramente a queda
        elif deslocamento < 0:
            deslocamento -= 2

        # Atualiza a posição y do pássaro
        self.y += deslocamento

        # angulo do passaro
        # Se estiver subindo ou logo após o pulo, rotaciona para cima (ângulo máximo)
        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA
        # Se estiver caindo, rotaciona para baixo (até -90 graus)
        else:
            if self.angulo > -90:
                self.angulo -= self.VELOCIDADE_ROTACAO

    # Desenha o pássaro na tela, incluindo a animação das asas e a rotação
    def desenhar(self, tela):
        # definir qual imagem do passaro vai usar
        # Incrementa o contador para controlar a animação
        self.contagem_imagem += 1

        # animação de batida de asa do passaro
        # Sequência de verificação do contador para alternar entre as imagens do pássaro (batida de asa)
        if self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 2:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 3:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 4:
            self.imagem = self.IMGS[1]
        # Reinicia o ciclo de animação
        elif self.contagem_imagem >= self.TEMPO_ANIMACAO * 4 + 1:
            self.imagem = self.IMGS[0]
            self.contagem_imagem = 0

        # se o passaro tiver caindo não vai bater asa
        # Força o pássaro a usar a imagem de asa aberta (plana) quando em queda acentuada
        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            self.contagem_imagem = self.TEMPO_ANIMACAO * 2

        # desenhar a imagem
        # Rotaciona a imagem atual do pássaro
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        # Obtém o centro da imagem original
        pos_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
        # Cria o retângulo da imagem rotacionada, centralizado na posição original
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)
        # Desenha a imagem rotacionada na tela
        tela.blit(imagem_rotacionada, retangulo.topleft)

    # Retorna a máscara de colisão do pássaro (usada para detecção precisa)
    def get_mask(self):
        pygame.mask.from_surface(self.imagem)


# Classe que representa o cano
class Cano:
    # Define a distância vertical entre o cano de cima e o de baixo
    DISTANCIA = 200
    # Define a velocidade horizontal de movimento dos canos
    VELOCIDADE = 5

    # Construtor da classe: inicializa o cano na posição x
    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        # Define as imagens do cano de cima (invertida) e de baixo
        self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True)
        self.CANO_BASE = IMAGEM_CANO
        self.passou = False  # Flag para saber se o pássaro já passou por este cano
        self.definir_altura()

    # Gera a altura aleatória para o buraco do cano e calcula as posições
    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        # Calcula a posição y do topo do cano de cima
        self.pos_base = self.altura - self.CANO_TOPO.get_height()
        # Calcula a posição y da base do cano de baixo (com a distância definida)
        self.pos_base = self.altura + self.DISTANCIA

    # Move o cano horizontalmente para a esquerda
    def mover(self):
        self.x -= self.VELOCIDADE

    # Desenha o cano (topo e base) na tela
    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))

    # Verifica se o pássaro colidiu com o cano (topo ou base)
    def colidir(self, passaro):
        # Obtém as máscaras de colisão
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        # Calcula a distância (offset) entre o pássaro e o topo/base do cano
        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        # Verifica se as máscaras se sobrepõem (colisão)
        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        # Retorna True se houver colisão
        if base_ponto or topo_ponto:
            return True
        # Retorna False se não houver colisão
        else:
            return False


# Classe que representa o chão
class Chao:
    # Define a velocidade de movimento do chão (igual à do cano)
    VELOCIDADE = 5
    # Obtém a largura da imagem do chão
    LARGURA = IMAGEM_CHAO.get_width()
    # Atribui a imagem do chão
    IMAGEM = IMAGEM_CHAO

    # Construtor da classe: inicializa o chão na posição y
    def __init__(self, y):
        self.y = y
        self.x1 = 0  # Posição x da primeira imagem do chão
        self.x2 = self.LARGURA  # Posição x da segunda imagem do chão

    # Move o chão horizontalmente para criar a ilusão de movimento contínuo (looping)
    def mover(self):
        # Move as duas imagens do chão para a esquerda
        self.x1 -= self.VELOCIDADE
        self.x2 -= self.VELOCIDADE

        # Reposiciona a primeira imagem quando ela sai totalmente da tela
        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x2 + self.LARGURA
        # Reposiciona a segunda imagem quando ela sai totalmente da tela
        if self.x2 + self.LARGURA < 0:
            self.x2 = self.x1 + self.LARGURA

    # Desenha as duas imagens do chão na tela para criar o efeito de loop
    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x1, self.y))
        tela.blit(self.IMAGEM, (self.x2, self.y))


# Função principal para desenhar todos os elementos do jogo na tela
def desenhar_tela(tela, passaros, canos, chao, pontos):
    # Desenha a imagem de fundo na posição (0, 0)
    tela.blit(IMAGEM_BACKGROUND, (0, 0))

    # Itera e desenha todos os pássaros (útil para múltiplos jogadores/IA)
    for passaro in passaros:
        passaro.desenhar(tela)

    # Itera e desenha todos os canos ativos na tela
    for cano in canos:
        cano.desenhar(tela)

    # Renderiza o texto da pontuação
    texto = FONTE_PONTOS.render(f"Pontuação: {pontos}", 1, (255, 255, 255))
    # Desenha o texto da pontuação no canto superior direito
    tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10))
    # Desenha o chão
    chao.desenhar(tela)
    # Atualiza toda a tela para exibir as alterações
    pygame.display.update()


def main():
    passaros = [Passaro(230, 350)]
    chao = Chao(250)
    canos = [Cano(700)]
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pontos = 0
    relogio = pygame.time.Clock()

