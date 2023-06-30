import os
from random import choice, randrange
from sys import exit

import pygame
from pygame.locals import *


def exibeMensagem(msg, tamanho, cor):
    fonte = pygame.font.SysFont('comicsansms', tamanho, True, False)
    mensagem = f'{msg}'
    texto_formatado = fonte.render(mensagem, True, cor)
    return texto_formatado


def reiniciar_jogo():
    global pontos, VEL_JOGO, colidiu, escolha_obstaculo
    pontos = 0
    VEL_JOGO = 0
    colidiu = False
    escolha_obstaculo = choice([0, 1])
    cacto.rect.x = lar
    dinovoador.rect.x = lar
    dino.rect.center = (100, alt - 64)
    dino.pulo = False


dir_imagens = './imagens/'
dir_sons = './sons/'

pontos = 0
lar, alt = 640, 480
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
ALT_SALTO = 250
VEL_SALTO = 15
VEL_NUVENS = 2
VEL_CHAO = 10
VEL_CACTO = 10
VEL_DINOVOADOR = 10
VEL_JOGO = 0
colidiu = False
escolha_obstaculo = choice([0, 1])

pygame.init()
pygame.mixer.init()

som_colisao = pygame.mixer.Sound('./sons/death_sound.wav')
som_colisao.set_volume(1)
som_pontuação = pygame.mixer.Sound('./sons/score_sound.wav')
som_pontuação.set_volume(1)

tela = pygame.display.set_mode((lar, alt))
pygame.display.set_caption("Dino's Game")

sprite_sheet = pygame.image.load(
    './imagens/dinoSpritesheet.png').convert_alpha()


class Dino(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.som_pulo = pygame.mixer.Sound('./sons/jump_sound.wav')
        self.som_pulo.set_volume(1)
        self.imagens_dino = []
        for i in range(3):
            img = sprite_sheet.subsurface((32 * i, 0), (32, 32))
            img = pygame.transform.scale(img, (32 * 3, 32 * 3))
            self.imagens_dino.append(img)
        self.index_lista = 0
        self.image = self.imagens_dino[self.index_lista]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (100, alt - 64)
        self.pulo = False

    def pular(self):
        self.pulo = True
        self.som_pulo.play()

    def update(self):
        if self.pulo:
            if self.rect.y <= ALT_SALTO:
                self.pulo = False
            self.rect.y -= VEL_SALTO
        else:
            if self.rect.y < (alt-64-96//2):
                self.rect.y += VEL_SALTO
            else:
                self.rect.y = alt-64-96//2

        if self.index_lista > 2:
            self.index_lista = 0
        self.index_lista += 0.25
        self.image = self.imagens_dino[int(self.index_lista)]


class Nuvens(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((32 * 7, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32 * 3, 32 * 3))
        self.rect = self.image.get_rect()
        self.rect.y = randrange(50, 200, 10)
        self.rect.x = randrange(100, 600, 50)

    def update(self):
        self.rect.x -= VEL_NUVENS + VEL_JOGO
        if self.rect.topright[0] < 0:
            self.rect.y = randrange(50, 200, 10)
            self.rect.x = randrange(lar, lar + 100, 40)


class Chao(pygame.sprite.Sprite):
    def __init__(self, pos_x):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((32 * 6, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32 * 2, 32 * 2))
        self.rect = self.image.get_rect()
        self.rect.y = alt - 64
        self.rect.x = pos_x * 64

    def update(self):
        self.rect.x -= VEL_CHAO + VEL_JOGO
        if self.rect.topright[0] < 0:
            self.rect.x = lar


class Cacto(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((32 * 5, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32 * 2, 32 * 2))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.escolha = escolha_obstaculo
        self.rect.center = (lar, alt - 64)
        self.rect.x = lar

    def update(self):
        if self.escolha == 1:
            self.rect.x -= VEL_CACTO + VEL_JOGO
            if self.rect.topright[0] < 0:
                self.rect.x = lar


class DinoVoador(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagens_dinovoador = []
        for i in range(3, 5):
            img = sprite_sheet.subsurface((32 * i, 0), (32, 32))
            img = pygame.transform.scale(img, (32 * 3, 32 * 3))
            self.imagens_dinovoador.append(img)

        self.index_lista = 0
        self.image = self.imagens_dinovoador[self.index_lista]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.escolha = escolha_obstaculo
        self.rect.center = (lar, 280)
        self.rect.x = lar

    def update(self):
        if self.escolha == 0:
            self.rect.x -= VEL_DINOVOADOR + VEL_JOGO
            if self.rect.topright[0] < 0:
                self.rect.x = lar

            if self.index_lista > 1:
                self.index_lista = 0
            self.index_lista += 0.25
            self.image = self.imagens_dinovoador[int(self.index_lista)]


todas_as_sprites = pygame.sprite.Group()
grupo_obstaculos = pygame.sprite.Group()

dino = Dino()
todas_as_sprites.add(dino)

for i in range(4):
    nuvem = Nuvens()
    todas_as_sprites.add(nuvem)

for i in range(lar//10):
    chao = Chao(i)
    todas_as_sprites.add(chao)

cacto = Cacto()
todas_as_sprites.add(cacto)
grupo_obstaculos.add(cacto)

dinovoador = DinoVoador()
todas_as_sprites.add(dinovoador)
grupo_obstaculos.add(dinovoador)

relogio = pygame.time.Clock()

while True:
    relogio.tick(30)
    tela.fill(BRANCO)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == KEYDOWN:
            if event.key == K_SPACE and not colidiu:
                if dino.rect.y != (alt-64-96//2):
                    pass
                else:
                    dino.pular()

            if event.key == K_r and colidiu:
                reiniciar_jogo()

    colisoes = pygame.sprite.spritecollide(
        dino, grupo_obstaculos, False, pygame.sprite.collide_mask)

    todas_as_sprites.draw(tela)

    if cacto.rect.topright[0] <= 6 or dinovoador.rect.topright[0] <= 6:
        escolha_obstaculo = choice([0, 1])
        cacto.rect.x, dinovoador.rect.x = lar, lar
        cacto.escolha, dinovoador.escolha = escolha_obstaculo, escolha_obstaculo

    if colisoes and not colidiu:
        som_colisao.play()
        colidiu = True

    if colidiu:
        if pontos % 100 == 0:
            pontos += 1
        gameover = exibeMensagem('GAME OVER!', 40, PRETO)
        restartmsg = exibeMensagem('Pressione R para reiniciar', 20, PRETO)
        tela.blit(gameover, (lar//2, alt//2))
        tela.blit(restartmsg, (lar//2, alt//2+45))
    else:
        pontos += 1
        todas_as_sprites.update()
        textopontos = exibeMensagem(pontos, 40, PRETO)

    if pontos % 100 == 0:
        som_pontuação.play()
        if VEL_JOGO >= 23:
            VEL_JOGO += 0
        else:
            VEL_JOGO += 1

    tela.blit(textopontos, (520, 30))
    pygame.display.flip()
