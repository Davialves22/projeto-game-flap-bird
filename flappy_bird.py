import pygame
import os
import random
import sys

# Configurações básicas
TELA_LARGURA = 500
TELA_ALTURA = 800

pygame.init()
pygame.font.init()

# Imagens
IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
IMAGEM_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
IMAGENS_PASSARO = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png')))
]

# Fontes
FONTE_PONTOS = pygame.font.SysFont('arial', 50, bold=True)
FONTE_GAME_OVER = pygame.font.SysFont('arialblack', 80)
FONTE_BOTAO = pygame.font.SysFont('arial', 40, bold=True)


class Passaro:
    IMGS = IMAGENS_PASSARO
    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagem = 0
        self.imagem = self.IMGS[0]

    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo ** 2) + self.velocidade * self.tempo

        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento

        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA
        else:
            if self.angulo > -90:
                self.angulo -= self.VELOCIDADE_ROTACAO

    def desenhar(self, tela):
        self.contagem_imagem += 1

        if self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 2:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 3:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 4:
            self.imagem = self.IMGS[1]
        else:
            self.imagem = self.IMGS[0]
            self.contagem_imagem = 0

        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            self.contagem_imagem = self.TEMPO_ANIMACAO * 2

        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        pos_centro = self.imagem.get_rect(topleft=(self.x, self.y)).center
        ret = imagem_rotacionada.get_rect(center=pos_centro)
        tela.blit(imagem_rotacionada, ret.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)


class Cano:
    DISTANCIA = 200
    VELOCIDADE = 5

    def __init__(self, x):
        self.x = x
        self.definir_altura()
        self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True)
        self.CANO_BASE = IMAGEM_CANO
        self.passou = False

    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.pos_topo = self.altura - IMAGEM_CANO.get_height()
        self.pos_base = self.altura + self.DISTANCIA

    def mover(self):
        self.x -= self.VELOCIDADE

    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))

    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        dist_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        dist_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        topo_ponto = passaro_mask.overlap(topo_mask, dist_topo)
        base_ponto = passaro_mask.overlap(base_mask, dist_base)

        return topo_ponto or base_ponto


class Chao:
    VELOCIDADE = 5
    LARGURA = IMAGEM_CHAO.get_width()
    IMAGEM = IMAGEM_CHAO

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.LARGURA

    def mover(self):
        self.x1 -= self.VELOCIDADE
        self.x2 -= self.VELOCIDADE
        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x2 + self.LARGURA
        if self.x2 + self.LARGURA < 0:
            self.x2 = self.x1 + self.LARGURA

    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x1, self.y))
        tela.blit(self.IMAGEM, (self.x2, self.y))


def desenhar_tela(tela, passaros, canos, chao, pontos):
    tela.blit(IMAGEM_BACKGROUND, (0, 0))
    for passaro in passaros:
        passaro.desenhar(tela)
    for cano in canos:
        cano.desenhar(tela)

    texto = FONTE_PONTOS.render(f"Pontos: {pontos}", 1, (255, 255, 255))
    tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10))
    chao.desenhar(tela)
    pygame.display.update()


def tela_game_over(tela, pontos):
    # Fundo escurecido
    overlay = pygame.Surface((TELA_LARGURA, TELA_ALTURA))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    tela.blit(overlay, (0, 0))

    # Textos menores e centralizados
    FONTE_GAME_OVER = pygame.font.SysFont('arialblack', 60)
    FONTE_PONTOS = pygame.font.SysFont('arial', 35, bold=True)
    FONTE_BOTAO = pygame.font.SysFont('arial', 28, bold=True)

    texto_game_over = FONTE_GAME_OVER.render("GAME OVER", True, (255, 0, 0))
    texto_rect = texto_game_over.get_rect(center=(TELA_LARGURA / 2, TELA_ALTURA / 2 - 120))
    tela.blit(texto_game_over, texto_rect)

    texto_pontos = FONTE_PONTOS.render(f"Sua Pontuação: {pontos}", True, (255, 255, 255))
    texto_pontos_rect = texto_pontos.get_rect(center=(TELA_LARGURA / 2, TELA_ALTURA / 2 - 50))
    tela.blit(texto_pontos, texto_pontos_rect)

    # Botões menores e mais elegantes
    botao_largura = 220
    botao_altura = 50
    espacamento = 20

    botao_jogar = pygame.Rect(TELA_LARGURA / 2 - botao_largura / 2, TELA_ALTURA / 2 + 10, botao_largura, botao_altura)
    botao_sair = pygame.Rect(TELA_LARGURA / 2 - botao_largura / 2, botao_jogar.bottom + espacamento, botao_largura,
                             botao_altura)

    pygame.draw.rect(tela, (50, 200, 50), botao_jogar, border_radius=12)
    pygame.draw.rect(tela, (200, 50, 50), botao_sair, border_radius=12)

    texto_jogar = FONTE_BOTAO.render("Jogar Novamente", True, (255, 255, 255))
    texto_sair = FONTE_BOTAO.render("Sair", True, (255, 255, 255))

    tela.blit(texto_jogar,
              (botao_jogar.centerx - texto_jogar.get_width() / 2, botao_jogar.centery - texto_jogar.get_height() / 2))
    tela.blit(texto_sair,
              (botao_sair.centerx - texto_sair.get_width() / 2, botao_sair.centery - texto_sair.get_height() / 2))

    pygame.display.update()

    # Loop da tela de fim
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_jogar.collidepoint(evento.pos):
                    main()  # Reinicia o jogo
                elif botao_sair.collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()


def main():
    passaros = [Passaro(230, 350)]
    chao = Chao(730)
    canos = [Cano(700)]
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pontos = 0
    relogio = pygame.time.Clock()

    rodando = True
    while rodando:
        relogio.tick(30)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                for passaro in passaros:
                    passaro.pular()

        for passaro in passaros:
            passaro.mover()
        chao.mover()

        adicionar_cano = False
        remover_canos = []
        for cano in canos:
            for i, passaro in enumerate(passaros):
                if cano.colidir(passaro):
                    tela_game_over(tela, pontos)
                if not cano.passou and passaro.x > cano.x:
                    cano.passou = True
                    adicionar_cano = True
            cano.mover()
            if cano.x + IMAGEM_CANO.get_width() < 0:
                remover_canos.append(cano)

        if adicionar_cano:
            pontos += 1
            canos.append(Cano(600))
        for cano in remover_canos:
            canos.remove(cano)

        for i, passaro in enumerate(passaros):
            if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                tela_game_over(tela, pontos)

        desenhar_tela(tela, passaros, canos, chao, pontos)


if __name__ == '__main__':
    main()
