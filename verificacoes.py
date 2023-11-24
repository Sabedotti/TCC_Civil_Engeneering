dim_minima_secao = 14

def pilar_pilarParede(dim_x, dim_y):
    if dim_y > dim_x:
        if dim_y > (dim_x * 5):
            return (1, f'As dimensões do pilar o tornam um pilar-parede. ' 
                    f'{dim_y} cm é maior que 5 * {dim_x} cm. '
                    f'Este programa abrange apenas pilares normais.')
        
    if dim_x > (dim_y * 5):
        return (1, f'As dimensões do pilar o tornam um pilar-parede. '
                f'{dim_x} cm é maior que 5 * {dim_y} cm. '
                'Este programa abrange apenas pilares normais.')
    
    return (0, f'O pilar a ser estudado é um pilar normal, e não um pilar parede.')

def dimensao_minima(dim_x, dim_y):
    if dim_x < dim_minima_secao and dim_y < dim_minima_secao:
        return (1, f'Ambas as dimensões X e Y da seção transversal são inferiores à dimensão permitida pela ABNT NBR 6118, de 14 cm')
    if dim_x < dim_minima_secao:
        return (1, f'A dimensão x, de {dim_x} cm é menor que a mínima permitida pela ABNT NBR 6118 ({dim_minima_secao} cm)')
    if dim_y < dim_minima_secao:
        return (1, f'A dimensão y, de {dim_y} cm é menor que a mínima permitida pela ABNT NBR 6118 ({dim_minima_secao} cm)')
    if (dim_x * dim_y) < 360:
        return(1, f'A seção transversal precisar ter área de pelo menos 360 cm². A seção informada possui {dim_x*dim_y} cm²')
    return (0, f'As dimensões x e y estão dentro dos parâmetros da ABNT NBR 6118. ' 
            'Apenas lembre que, para pilares que possuem dimensão entre 14 e 19 cm, '  
            'deve ser considerado coeficiente adicional γn para esforços solicitantes de cálculo.')

def eq_area_minima(dim_x, dim_y):
    minima = dim_x * dim_y * 0.004
    return (0, f'A área de aço mínima de armaduras longitudinais para a seção é de {round(minima, 3)} cm², equivalente a 0,004 * Ac (ou 0,15*Nd/fyd, inferior a 0,04*Ac)')

def area_minima_armadura_verif(area_armadura, dim_x, dim_y):
    minima = dim_x * dim_y * 0.004
    area_de_armadura = area_armadura
    if area_de_armadura >= minima:
        return (0, f'A área de armaduras longitudinais da seção ({round(area_de_armadura, 3)} cm²) é MAIOR que a área mínima trazida pela norma ({minima} cm²)')
    else:
        return (1, f'A área de armaduras longitudinais da seção ({round(area_de_armadura,3)} cm²) é MENOR que a área mínima trazida pela norma ({minima} cm²)')

def eq_area_maxima(dim_x, dim_y):
    area_concreto = dim_x * dim_y
    area_maxima_permitida = 8 / 100 * area_concreto
    return (0, f'A área de aço máxima de armaduras longitudinais para a seção é de {round(area_maxima_permitida, 3)} cm², equivalente a 0,08 * Ac, porém considera-se 0,04*Ac devido às emendas. Desta forma, a área de aço máximo a ser considerada é igual {round(area_maxima_permitida/2, 3)} cm²')

def area_maxima_armadura_verif(area_armadura, dim_x, dim_y):
    area_de_armadura = area_armadura
    area_concreto = dim_x * dim_y
    area_maxima_permitida = 4 / 100 * area_concreto
    if area_de_armadura <= area_maxima_permitida:
        return (0, f'A área de armaduras longitudinais da seção ({round(area_de_armadura, 3)} cm²) é MENOR que a área máxima trazida pela norma ({round(area_maxima_permitida, 3)} cm²).')
    else:
        return (1, f'A área de armaduras longitudinais da seção ({round(area_de_armadura, 3)} cm²) é MAIOR que a área máxima trazida pela norma ({round(area_maxima_permitida, 3)} cm²).')

def espacamentos_entre_barras(dim_x, dim_y, nx, ny, d_linha, bitola_armadura_longitudinal):
    bitola = bitola_armadura_longitudinal / 10
    # para dimensao em x
    bs_x = dim_x - (2 * d_linha) + bitola
    espacamento_existente_x = (bs_x - (nx * bitola)) / (nx - 1)

    # para dimensao em y
    bs_y = dim_y - (2 * d_linha) + bitola
    espacamento_existente_y = (bs_y - (ny * bitola)) / (ny - 1)

    return (espacamento_existente_x, espacamento_existente_y)

def espacamento_maximo_entre_barras(dim_x, dim_y, espaco_entre_barras, sentido):
    if dim_x < dim_y:
        menor_dimensao = dim_x
    else:
        menor_dimensao = dim_y
    
    maximos = [(2 * menor_dimensao), 40]
    esp_maximo = min(maximos)
    frase_1 = (f'O espacamento entre barras no sentido {sentido} ({espaco_entre_barras} cm) é maior do que o máximo permitido pela ABNT NBR 6118 ({esp_maximo} cm).')
    frase_2 = (f'O espacamento entre barras no sentido {sentido} ({espaco_entre_barras} cm) é menor ou igual ao máximo permitido pela ABNT NBR 6118 ({esp_maximo} cm).')

    if espaco_entre_barras > esp_maximo:
        return (1, frase_1)
    else:
        return (0, frase_2)

def espacamento_minimo_entre_barras(diam_barra, espacamento_entre_barras, diam_agregado, sentido):
    minimos = [2, diam_barra/10, 1.2 * diam_agregado / 10]
    esp_minimo = max(minimos)

    frase_1 = (f'O espaçamento no sentido {sentido} ({espacamento_entre_barras} cm) é maior que o espaçamento mínimo permitido pela ABNT NBR 6118 ({esp_minimo} cm)')
    frase_2 = (f'O espaçamento no sentido {sentido} ({espacamento_entre_barras} cm) é menor que o espaçamento mínimo permitido pela ABNT NBR 6118 ({esp_minimo} cm)')

    if espacamento_entre_barras > esp_minimo:
        return (0, frase_1)
    else:
        return (1, frase_2)

def verif_bitola(bitola, dim_x, dim_y):
    menor_dimensao = dim_x
    if dim_y < dim_x:
        menor_dimensao = dim_y
    limite_superior = menor_dimensao / 8

    if bitola < 10:
        return (1, f'A bitola da seção transversal informada ({bitola}) é menor que a dimensão mínima indicada pela ABNT NBR 6118 (10 mm)')

    if bitola/10 > limite_superior:
        return (1, f'A bitola da seção transversal informada ({bitola}) é maior que a dimensão máxima indicada pela ABNT NBR 6118 ({limite_superior} mm), que é 1/8 da menor dimensão trasnversal.')

    return (0, f'A bitola da seção trasnversal informada está dentro das indicações feitas pela ABNT NBR 6118')

def mensagens_consideracoes_st(dim_x, dim_y, area_armadura, espacamento_entre_barras_x, espacamento_entre_barras_y, bitola, diam_agregado_mm):
    verif_1 = pilar_pilarParede(dim_x, dim_y)
    verif_2 = dimensao_minima(dim_x, dim_y)
    verif_3 = eq_area_minima(dim_x, dim_y)
    verif_4 = area_minima_armadura_verif(area_armadura, dim_x, dim_y)
    verif_5 = eq_area_maxima(dim_x, dim_y)
    verif_6 = area_maxima_armadura_verif(area_armadura, dim_x, dim_y)
    verif_7 = espacamento_maximo_entre_barras(dim_x, dim_y, espacamento_entre_barras_x, "x")
    verif_8 = espacamento_maximo_entre_barras(dim_x, dim_y, espacamento_entre_barras_y, "y")
    verif_9 = espacamento_minimo_entre_barras(bitola, espacamento_entre_barras_x, diam_agregado_mm, 'x')
    verif_10 = espacamento_minimo_entre_barras(bitola, espacamento_entre_barras_y, diam_agregado_mm, 'y')
    verif_11 = verif_bitola(bitola, dim_x, dim_y)
    lista = [verif_1, verif_2, verif_3, verif_4, verif_5, verif_6, verif_7, verif_8, verif_9, verif_10, verif_11]

    return lista