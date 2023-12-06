import cv2
import numpy as np
from calculos import posicionamento_das_barras


def desenho_secao_transversal_pilar(dim_x, dim_y, nx, ny, d_linha, bitola_aco):
    # inicialização do desenho
    largura_fundo_x = 304
    largura_fundo_y = largura_fundo_x
    referencia = 0.90 * largura_fundo_x
    # imagem 400x300, com fundo branco e 3 canais para as cores
    canvas = np.ones((largura_fundo_x, largura_fundo_y, 3)) * 255
    cv2.waitKey(0)
    maior_face = dim_x
    if dim_y > dim_x:
        maior_face = dim_y

    multiplicador = (referencia / maior_face)

    # cores
    azul = (255, 0, 0)
    vermelho = (0, 0, 255)

    # Posicionamento das barras e das faces do pilar
    posicao_barras = posicionamento_das_barras(dim_x, dim_y, nx, ny, d_linha)
    p1x, p1y = int(largura_fundo_x/2 - dim_x / 2 * multiplicador), \
        int(largura_fundo_y/2 + dim_y / 2 * multiplicador)
    p2x, p2y = int(p1x + dim_x * multiplicador), int(p1y)
    p3x, p3y = int(p1x), int(p1y - dim_y * multiplicador)
    p4x, p4y = int(p1x + dim_x * multiplicador), \
        int(p1y - dim_y * multiplicador)

    # desenho das faces
    cv2.line(canvas, (p1x, p1y), (p2x, p2y), azul, 2)
    cv2.line(canvas, (p1x, p1y), (p3x, p3y), azul, 2)
    cv2.line(canvas, (p2x, p2y), (p4x, p4y), azul, 2)
    cv2.line(canvas, (p3x, p3y), (p4x, p4y), azul, 2)

    # desenho das armaduras
    for num_armadura, coord_x, coord_y in posicao_barras:
        int_coord_x = int(p1x + coord_x * multiplicador)
        int_coord_y = int(p1y - coord_y * multiplicador)
        cv2.circle(canvas, (int_coord_x, int_coord_y),
                   (int(bitola_aco / 20 * multiplicador)), vermelho, -1)

    # cv2.imshow(f'Pilar {dim_x} x {dim_y}, nx={nx}, ny={ny}', canvas)
    cv2.imwrite('programa_tcc\\imagem_nova.png', canvas)
    cv2.waitKey(0)
