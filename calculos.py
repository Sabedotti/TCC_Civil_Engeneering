import copy
from math import pi as pi
from math import (acos)

# Definições FCk e FCd
def calculo_fcd(fck, gama_c):
    fcd = fck / gama_c
    return fcd

def calculo_fyd(fyk, gama_s):
    fyd = fyk / gama_s
    return fyd

def valor_n(fck):
    if fck <= 50:
        coeficiente_n = 2
    else:
        coeficiente_n = 1.4 + (23.4 * (((90 - fck)/100) ** 4))

    return float(coeficiente_n)

def ec2_ecu(fck):
    if fck <= 50:
        ec2 = (2 / 1000)
        ecu = (3.5 / 1000)

    if 55 <= fck < 90:
        ec2 = float((2 / 1000) + (0.085/1000) * ((fck - 50) ** 0.53))
        ecu = float((2.6 / 1000) + (35/1000) * (((90 - fck) / 100) ** 4))

    if fck == 90:
        ec2 = 2.6 / 1000
        ecu = ec2

    return ec2, ecu

def tensao_concreto(deformacao, ec2, fcd, n):
    if deformacao <= ec2:
        tensao = 0.85 * fcd * (1- ((1-(deformacao / ec2)) ** n))
    else:
        tensao = 0.85 * fcd
    return tensao

def determinacao_coef_eta_c(fck):
    coef_eta_c = 1
    if fck > 40:
        coef_eta_c = (40 / fck) ** (1 / 3)
    return coef_eta_c

def tensao_concreto_2023(fck, deformacao, ec2, fcd, n):
    coef_eta_c = 1
    if fck > 40:
        coef_eta_c = (40 / fck) ** (1 / 3)

    if deformacao <= ec2:
        tensao = 0.85 * coef_eta_c * fcd * (1- ((1-(deformacao / ec2)) ** n))
    else:
        tensao = 0.85 * coef_eta_c * fcd
        
    return tensao

# Dados para gráficos
def diagrama_tensao_deformacao_concreto(ec2, ecu, fck, gama_c):
    fcd = calculo_fcd(fck, gama_c) / 10    #kn/cm²
    coef_n = valor_n(fck)
    deformacao = 0
    passo = 0.001/1000
    lista_x = []
    lista_y = []

    while deformacao <= ecu:
        tensao = tensao_concreto(deformacao, ec2, fcd, coef_n)
        lista_x.append(deformacao * 1000)
        lista_y.append(tensao)
        deformacao += passo

    # unidade kN/cm²
    return lista_x, lista_y

def diagrama_tensao_deformacao_concreto_2023(ec2, ecu, fck, gama_c):
    fcd = calculo_fcd(fck, gama_c) / 10    #kn/cm²
    coef_n = valor_n(fck)
    deformacao = 0
    passo = 0.001/1000
    lista_x = []
    lista_y = []

    while deformacao <= ecu:
        tensao = tensao_concreto_2023(fck, deformacao, ec2, fcd, coef_n)
        lista_x.append(deformacao * 1000)
        lista_y.append(tensao)
        deformacao += passo

    # unidade kN/cm²
    return lista_x, lista_y

def diagrama_tensao_deformacao_aco(fyd, es, ecu, mod_elasticidade):
    i = ecu * (-1)
    passo = 0.001/1000
    eyd = fyd / mod_elasticidade
    eyd_linha = eyd * (-1)    
    lista_x = []
    lista_y = []
    i_eyd = eyd_linha 

    while i <= es:
        if i <= eyd_linha:
            tensao = fyd * (-1) / 10

        elif i <= eyd:
            tensao = mod_elasticidade * i_eyd / 10
            i_eyd += passo
    
        else:
            tensao = fyd / 10
    
        lista_x.append(i * 1000)
        lista_y.append(tensao)
        i += passo

    return lista_x, lista_y

#Posição das barras, com referência 0,0 no canto inferior esquerdo
def posicionamento_das_barras(dim_x, dim_y, nx, ny, d_linha):
    numero_de_barras = (2 * nx) + 2 * (ny - 2)
    primeira_linha_x = d_linha
    primeira_linha_y = d_linha
    ultima_linha_x = dim_x - d_linha
    ultima_linha_y = dim_y - d_linha
    distancias_entre_barras_x = (ultima_linha_x - primeira_linha_x) / (nx - 1)
    distancias_entre_barras_y = (ultima_linha_y - primeira_linha_y) / (ny - 1)
    barra = 1
    posicao_barras = []
    coordenada_x = primeira_linha_x
    coordenada_y = primeira_linha_y

    while barra <= numero_de_barras:
        posicao_barras.append((barra, coordenada_x, coordenada_y))

        if barra < nx:
            coordenada_x += distancias_entre_barras_x
        
        elif barra == nx:
            coordenada_x = primeira_linha_x
            coordenada_y += distancias_entre_barras_y
            i = 0
        
        elif barra <= (numero_de_barras - nx):
            if i == 0:
                i += 1
                coordenada_x = ultima_linha_x
            
            elif i == 1:
                i -= 1
                coordenada_x = primeira_linha_x
                coordenada_y += distancias_entre_barras_y
        else:
            coordenada_x += distancias_entre_barras_x
        
        barra += 1
    return posicao_barras

def determinacao_area_bitolas_compressao_concreto(bitola_aco, passo):
    i = passo
    bitola = bitola_aco / 10   #cm
    area_inteira = ((bitola / 2) ** 2) * pi
    areas = []
    hipotenusa = bitola / 2

    while i <= hipotenusa:

        catet_adj = hipotenusa - i
        cateto_oposto = ((hipotenusa ** 2) - (catet_adj ** 2)) ** (1/2)
        angulo = (acos(catet_adj / hipotenusa)) * 180 / pi
        area1 = area_inteira - (2 * angulo / 360 * area_inteira)
        area2 = catet_adj * cateto_oposto

        area_final = area_inteira - area1 - area2 - sum(areas)
        areas.append(area_final)
        i = round(i + passo, 8)

    areas2 = []
    areas2 += areas
    areas2.reverse()

    areas_total = areas + areas2
    return areas_total

def definicao_aco_area_compressao(posicao_barras, dim_xy, passo, bitola_aco):
    lista = []
    posicoes = []
    bitola = bitola_aco / 10  #cm
    i = 0
    area_de_aco = []
    
    for barra in posicao_barras:
        if barra not in posicoes:
            posicoes.append(barra)
            lista.append((barra - (bitola/2), posicao_barras.count(barra)))
    
    indice_1 = 0
    indice_2 = 0

    while i < dim_xy:
        if i > lista[indice_1][indice_2]:
            area_de_aco.append(0)
            i = round(i + passo, 4)

        if i < lista[indice_1][indice_2]:
            area_de_aco.append(0)
            i = round(i + passo, 4)
        
        elif i == lista[indice_1][indice_2]:
            # area_de_aco.append(0)
            lista_areas = determinacao_area_bitolas_compressao_concreto(bitola_aco, passo)
            
            for item in lista_areas:
                area_final = item * lista[indice_1][1]
                area_de_aco.append(area_final)
                i = round(i + passo, 4)

            if (indice_1 + 1) == len(lista):
                ...
            else:
                indice_1 += 1

    return area_de_aco

def coordenadas_xy_barras_aco(posicao_barras):
    coord_x = []
    coord_y = []
    for posicao in posicao_barras:
        coord_x.append(posicao[-2])
        coord_y.append(posicao[-1])

    return coord_x, coord_y

def areas_de_concreto(posicao_xy_barras, comp_secao, altura, bitola_aco):
    passo = 0.01
    areas_aco_secao = definicao_aco_area_compressao(posicao_xy_barras, comp_secao, passo, bitola_aco)
    i = passo
    indice = 0
    lista_areas_concreto = []

    while i <= comp_secao:
        area_concreto = (passo * altura) - areas_aco_secao[indice]
        lista_areas_concreto.append(area_concreto)
        i = round(i + passo, 4)
        indice += 1

    return lista_areas_concreto

def calc_compressao_concreto(bx, deformacao_maxima_para_bx, ec2, fcd, n, cg, comp_secao, areas_concreto):
    passo = 0.01
    i = passo
    areas_comp_concreto = areas_concreto

    if bx < comp_secao:
        fim_compressao = bx
    else:
        fim_compressao = comp_secao

    deformacao = deformacao_maxima_para_bx
    deformacao_por_passo = passo / bx * deformacao_maxima_para_bx
    indice_areas_concreto = 0
    lista_forcas = []
    lista_momentos = []

    while i <= fim_compressao:
        tensao = tensao_concreto(deformacao, ec2, fcd, n)
        area_de_compressao = areas_comp_concreto[indice_areas_concreto]
        forca = tensao * area_de_compressao
        deformacao -= deformacao_por_passo

        lista_forcas.append(forca)
        lista_momentos.append(forca * (cg - i + (passo/2)))

        indice_areas_concreto += 1
        i = round(i + passo, 4)

    return sum(lista_forcas), sum(lista_momentos)

# Área de testes compressão concreto atualizado

def area_por_passo_concreto(passo, larg_secao):
    area_passo_concreto = passo * larg_secao
    return area_passo_concreto    

def forcas_concreto(passo, bx, def_max_concreto, comp_secao, ec2, fcd, coef_n, area_concreto_por_passo, cg, fck):
    ln = bx
    fcd_cm = fcd / 10
    somat_forcas_normais = 0
    somat_momentos = 0
    somat_forcas_normais_2023 = 0
    somat_momentos_2023 = 0
    dist_momento = passo / 2
    def_por_passo = passo * def_max_concreto / ln
    def_0 = def_max_concreto
    def_1 = def_0 - def_por_passo
    i = 0
    i_max = comp_secao
    if ln < comp_secao:
        i_max = ln
    
    while i < i_max:
        deformacao_da_area = (def_0 + def_1) / 2
        tensao = tensao_concreto(deformacao_da_area, ec2, fcd_cm, coef_n)
        tensao_2023 = tensao_concreto_2023(fck, deformacao_da_area, ec2, fcd_cm, coef_n)
        forca_normal = tensao * area_concreto_por_passo
        forca_normal_2023 = tensao_2023 * area_concreto_por_passo
        somat_forcas_normais += forca_normal
        somat_forcas_normais_2023 +=forca_normal_2023
        momento = forca_normal * (cg - dist_momento)
        momento_2023 = forca_normal_2023 * (cg-dist_momento)
        somat_momentos += momento
        somat_momentos_2023 += momento_2023

        def_0 -= def_por_passo
        def_1 -= def_por_passo
        dist_momento = round(dist_momento + passo, 4)
        i = round(i + passo, 4)

    return somat_forcas_normais, somat_momentos, somat_forcas_normais_2023, somat_momentos_2023
    
def subtracao_area_aco_bitola(bitola_aco):
    bitola = bitola_aco / 10   #cm
    passo = 0.001
    area_bitola = ((bitola/2) ** 2) * pi
    lista_1 = []
    lista_2 = []
    hipotenusa = bitola / 2
    cateto_adj = bitola / 2
    somatorio_areas = 0
    num_iteracoes = bitola / 2 / passo
    i = 0
    while i < num_iteracoes:
        cateto_adj = round(cateto_adj - passo, 3)
        cateto_oposto = ((hipotenusa ** 2) - (cateto_adj ** 2)) ** (1/2)
        angulo = (acos(cateto_adj / hipotenusa)) * 180 / pi
        area1 = area_bitola - (2 * angulo / 360 * area_bitola)
        area2 = cateto_adj * cateto_oposto
        area_de_aco = area_bitola - (area1 + area2) - somatorio_areas
        somatorio_areas += area_de_aco

        lista_1.append(area_de_aco)
        lista_2.append(area_de_aco)
        i += 1
    lista_2.reverse()

    lista_areas_final = lista_1 + lista_2

    return lista_areas_final

def forcas_subtracao_areas_aco(pontos_centrais_aco, bitola_aco, bx, cg, def_max_concreto, ec2, fcd, coef_n, lista_areas_aco_para_subtracao, fck):
    bitola = bitola_aco/10
    ln = bx
    passo = 0.001
    areas_para_subtracao = lista_areas_aco_para_subtracao
    fcd_cm = fcd / 10   #cm
    deformacao_por_passo = passo * def_max_concreto / ln
    momento_total = 0
    f_normal_total = 0
    momento_total_2023 = 0
    f_normal_total_2023 = 0
    momento = 0
    forca_normal = 0
    momento_2023 = 0
    forca_normal_2023 = 0
    lista_aux = [-1]

    for item in pontos_centrais_aco:
        inicio_da_bitola = item - (bitola/2)
        fim_da_bitola = inicio_da_bitola + bitola
        
        if inicio_da_bitola >= ln:
            ...
        
        elif item == lista_aux[-1]:
            f_normal_total += f_normal_bitola
            momento_total += f_momento_bitola
            f_normal_total_2023 += f_normal_bitola_2023
            momento_total_2023 += f_momento_bitola_2023
            lista_aux.append(item)

        else:
            f_normal_bitola = 0
            f_momento_bitola = 0
            f_normal_bitola_2023 = 0
            f_momento_bitola_2023 = 0
            dist_momento = cg - (inicio_da_bitola + (passo / 2))
            i = 0
            fim_interacao = fim_da_bitola
            if ln < fim_interacao:
                fim_interacao = ln
            numero_iteracoes = round((fim_interacao - inicio_da_bitola) / passo, 0)
            def_0 = (ln - inicio_da_bitola) / ln * def_max_concreto
            def_1 = def_0 - deformacao_por_passo
            while i < numero_iteracoes:
                media_defs = (def_0 + def_1) / 2
                tensao = (tensao_concreto(media_defs, ec2, fcd_cm, coef_n))
                tensao_2023 = tensao_concreto_2023(fck, media_defs, ec2, fcd_cm, coef_n)
                forca_normal = tensao * areas_para_subtracao[i] * (-1)
                forca_normal_2023 = tensao_2023 * areas_para_subtracao[i] * (-1)
                momento = forca_normal * dist_momento
                momento_2023 = forca_normal_2023 * dist_momento
                f_normal_bitola += forca_normal
                f_momento_bitola += momento
                f_normal_bitola_2023 += forca_normal_2023
                f_momento_bitola_2023 += momento_2023
                i += 1
                def_0 - deformacao_por_passo
                def_1 - deformacao_por_passo
                dist_momento -= passo
            lista_aux.append(item)
            f_normal_total += f_normal_bitola
            momento_total += f_momento_bitola
            f_normal_total_2023 += f_normal_bitola_2023
            momento_total_2023 += f_momento_bitola_2023

    return f_normal_total, momento_total, f_normal_total_2023, momento_total_2023

def forca_concreto_total(pontos_centrais_aco, bitola_aco, bx, def_max_concreto, comp_secao, ec2, fcd, coef_n, area_concreto_por_passo, cg, lista_areas_aco_para_subtracao, fck):
    concreto_cheio_fn, concreto_cheio_momento, concreto_cheio_fn_2023, concreto_cheio_momento_2023 = forcas_concreto(0.01, bx, def_max_concreto, comp_secao, ec2, fcd, coef_n, area_concreto_por_passo, cg, fck)
    subtracao_areas_fn, subtracao_areas_momento, subtracao_areas_fn_2023, subtracao_areas_momento_2023 = forcas_subtracao_areas_aco(pontos_centrais_aco, bitola_aco, bx, cg, def_max_concreto, ec2, fcd, coef_n, lista_areas_aco_para_subtracao, fck)

    forca_normal_total = concreto_cheio_fn + subtracao_areas_fn
    forca_momento_total = concreto_cheio_momento + subtracao_areas_momento
    forca_normal_total_2023 = concreto_cheio_fn_2023 + subtracao_areas_fn_2023
    forca_momento_total_2023 = concreto_cheio_momento_2023 + subtracao_areas_momento_2023

    return(forca_normal_total, forca_momento_total, forca_normal_total_2023, forca_momento_total_2023)

def limite_tracao_max(posicao_primeira_barra, posicao_ultima_barra, fyd, mod_elasticidade, es):  #limite entre tração máxima e limite 1
    limite = posicao_ultima_barra + ((posicao_ultima_barra - posicao_primeira_barra) * es / ((fyd / mod_elasticidade) - es))
    return limite

def limite_1():   #limite entre domínios 1 e 2
    limite = 0
    return limite

def limite_2(ecu, es, posicao_ultima_barra):   #limite entre domínios 2 e 3
    limite = ecu / (ecu + es) * posicao_ultima_barra
    return limite

def limite_3(ecu, fyd, modulo_elasticidade, posicao_ultima_barra):   #limite entre domínios 3 e 4
    limite = ecu / (ecu + (fyd / modulo_elasticidade)) * posicao_ultima_barra
    return limite

def limite_4(ecu, posicao_ultima_barra):   #limite entre domínios 4 e 4a
    limite = ecu / ecu * posicao_ultima_barra
    return limite

def limite_4a(dimensao, d_linha, posicao_ultima_barra):   #limite entre domínios 4a e 5
    limite = dimensao / (dimensao - d_linha) * posicao_ultima_barra
    return limite

def limite_5(ec2, ecu, dimensao):
    limite = dimensao + (dimensao / 3 * 25)

    return limite

def calc_limite_tracaomax_1(bx_secao, posicao_xy_barras, dim_xy, es, fyd, bitola, mod_elasticidade):
    bx = bx_secao
    bx_calculos = bx * (-1)
    pos_barras = posicao_xy_barras
    ultima_linha_barras = max(pos_barras)
    bitola_aco = bitola / 10   #cm
    modulo_elasticidade = mod_elasticidade / 10   #kn/cm²
    fyd_cm = fyd / 10   #kn/cm²
    cg = dim_xy / 2
    forcas_normais = []
    forcas_momento = []
    
    for barra in pos_barras:
        area_de_aco = ((bitola_aco / 2) ** 2) * pi
        deslocamento_barra = (barra + bx_calculos) * es / (bx_calculos + ultima_linha_barras)
        tensao_tracao_aco = deslocamento_barra * modulo_elasticidade

        if tensao_tracao_aco > fyd_cm:
            tensao_tracao_aco = fyd_cm
            
        forca_normal_tracao = tensao_tracao_aco * area_de_aco
        forcas_normais.append(forca_normal_tracao)

        momento = forca_normal_tracao * (barra - cg)
        forcas_momento.append(momento / 100)   #kn*m
            
    return [sum(forcas_normais), sum(forcas_momento)], [sum(forcas_normais), sum(forcas_momento)]

def calc_limite_1_2(bx_indicado, posicao_xy_barras, bitola_aco, ec2, es, mod_elasticidade, fyd, dim_xy, fcd, coef_n, comp_secao, area_concreto_por_passo, lista_areas_aco_para_subtracao, fck):
    bx = bx_indicado
    bitola_cm = bitola_aco / 10   #cm
    pos_barras = posicao_xy_barras
    ultima_linha_barras = max(pos_barras)
    modulo_elasticidade = mod_elasticidade / 10   #kn/cm²
    fyd_cm = fyd / 10   #kn/cm²
    fcd_cm = fcd / 10   #kn/cm²
    cg = dim_xy / 2
    def_max_concreto = bx * es / (ultima_linha_barras - bx)
    forcas_normais = []
    forcas_momento = []
    forcas_normais_2023 = []
    forcas_momento_2023 = []
    forca_normal_concreto, forca_momento_concreto, forca_normal_concreto_2023, forca_momento_concreto_2023 = forca_concreto_total(posicao_xy_barras, bitola_aco, bx, def_max_concreto, comp_secao, ec2, fcd, coef_n, area_concreto_por_passo, cg, lista_areas_aco_para_subtracao, fck)
    forcas_normais.append(forca_normal_concreto)
    forcas_momento.append(forca_momento_concreto)
    forcas_normais_2023.append(forca_normal_concreto_2023)
    forcas_momento_2023.append(forca_momento_concreto_2023)

    for barra in pos_barras:
        area_de_aco = ((bitola_cm / 2) ** 2) * pi
        if barra < bx:
            deslocamento_barra = (bx - barra) * def_max_concreto / bx
        else:
            deslocamento_barra = (barra - bx) * es / (ultima_linha_barras - bx)

        tensao_tracao_aco = deslocamento_barra * modulo_elasticidade

        if tensao_tracao_aco > fyd_cm:
            tensao_tracao_aco = fyd_cm

        if barra < bx:
            forca_normal_aco = tensao_tracao_aco * area_de_aco
            forcas_normais.append(forca_normal_aco)
            forcas_normais_2023.append(forca_normal_aco)
            momento = forca_normal_aco * (cg - barra)
            forcas_momento.append(momento)
            forcas_momento_2023.append(momento)

        else:
            forca_normal_aco = tensao_tracao_aco * area_de_aco * (-1)
            forcas_normais.append(forca_normal_aco)
            forcas_normais_2023.append(forca_normal_aco)
            momento = forca_normal_aco * (cg - barra)
            forcas_momento.append(momento)
            forcas_momento_2023.append(momento)

    return [sum(forcas_normais) * (-1), sum(forcas_momento)/100], [sum(forcas_normais_2023) * (-1), sum(forcas_momento_2023)/100]

def calc_limite_2_3(bx_indicado, bitola_aco, posicao_xy_barras, mod_elasticidade, fyd, fcd, dim_xy, ecu, ec2, coef_n, comp_secao, area_concreto_por_passo, lista_areas_aco_para_subtracao, fck):
    bx = bx_indicado
    bitola_cm = bitola_aco / 10   #cm
    pos_barras = posicao_xy_barras
    modulo_elasticidade = mod_elasticidade / 10   #kn/cm²
    fyd_cm = fyd / 10   #kn/cm²
    fcd_cm = fcd / 10   #kn/cm²
    cg = dim_xy / 2
    def_max_concreto = ecu
    forcas_normais = []
    forcas_momento = []
    forcas_normais_2023 = []
    forcas_momento_2023 = []
    forca_normal_concreto, forca_momento_concreto, forca_normal_concreto_2023, forca_momento_concreto_2023 = forca_concreto_total(posicao_xy_barras, bitola_aco, bx, def_max_concreto, comp_secao, ec2, fcd, coef_n, area_concreto_por_passo, cg, lista_areas_aco_para_subtracao, fck)
    forcas_normais.append(forca_normal_concreto)
    forcas_momento.append(forca_momento_concreto)
    forcas_normais_2023.append(forca_normal_concreto_2023)
    forcas_momento_2023.append(forca_momento_concreto_2023)

    for barra in pos_barras:
        area_de_aco = ((bitola_cm / 2) ** 2) * pi

        if barra < bx:
            deslocamento_barra = (bx - barra) * ecu / bx
        else:
            deslocamento_barra = (barra - bx) * ecu / bx
        
        tensao_tracao_aco = deslocamento_barra * modulo_elasticidade
        if tensao_tracao_aco > fyd_cm:
            tensao_tracao_aco = fyd_cm
                
        if barra < bx:
            forca_normal_aco = tensao_tracao_aco * area_de_aco
            forcas_normais.append(forca_normal_aco)
            forcas_normais_2023.append(forca_normal_aco)
            momento = forca_normal_aco * (cg - barra)
            forcas_momento.append(momento)
            forcas_momento_2023.append(momento)

        else:
            forca_normal_aco = tensao_tracao_aco * area_de_aco * (-1)
            forcas_normais.append(forca_normal_aco)
            forcas_normais_2023.append(forca_normal_aco)
            momento = forca_normal_aco * (cg - barra)
            forcas_momento.append(momento)
            forcas_momento_2023.append(momento)

    return [sum(forcas_normais) * (-1), sum(forcas_momento)/100], [sum(forcas_normais_2023) * (-1), sum(forcas_momento_2023)/100]

def calc_limite_3_4(bx_indicado, bitola_aco, posicao_xy_barras, mod_elasticidade, fyd, fcd, dim_xy, ecu, ec2, coef_n, comp_secao, area_concreto_por_passo, lista_areas_aco_para_subtracao, fck):
    bx = bx_indicado
    bitola_cm = bitola_aco / 10   #cm
    pos_barras = posicao_xy_barras
    modulo_elasticidade = mod_elasticidade / 10   #kn/cm²
    fyd_cm = fyd / 10   #kn/cm²
    fcd_cm = fcd / 10   #kn/cm²
    cg = dim_xy / 2
    def_max_concreto = ecu
    forcas_normais = []
    forcas_momento = []
    forcas_normais_2023 = []
    forcas_momento_2023 = []
    forca_normal_concreto, forca_momento_concreto, forca_normal_concreto_2023, forca_momento_concreto_2023 = forca_concreto_total(posicao_xy_barras, bitola_aco, bx, def_max_concreto, comp_secao, ec2, fcd, coef_n, area_concreto_por_passo, cg, lista_areas_aco_para_subtracao, fck)
    forcas_normais.append(forca_normal_concreto)
    forcas_momento.append(forca_momento_concreto)
    forcas_normais_2023.append(forca_normal_concreto_2023)
    forcas_momento_2023.append(forca_momento_concreto_2023)

    for barra in pos_barras:
        area_de_aco = ((bitola_cm / 2) ** 2) * pi

        if barra < bx:
            deslocamento_barra = (bx - barra) * ecu / bx
        else:
            deslocamento_barra = (barra - bx) * ecu / bx
        
        tensao_tracao_aco = deslocamento_barra * modulo_elasticidade
        if tensao_tracao_aco > fyd_cm:
            tensao_tracao_aco = fyd_cm

        if barra < bx:
            forca_normal_aco = tensao_tracao_aco * area_de_aco
            forcas_normais.append(forca_normal_aco)
            forcas_normais_2023.append(forca_normal_aco)
            momento = forca_normal_aco * (cg - barra)
            forcas_momento.append(momento)
            forcas_momento_2023.append(momento)

        else:
            forca_normal_aco = tensao_tracao_aco * area_de_aco * (-1)
            forcas_normais.append(forca_normal_aco)
            forcas_normais_2023.append(forca_normal_aco)
            momento = forca_normal_aco * (cg - barra)
            forcas_momento.append(momento)
            forcas_momento_2023.append(momento)

    return [sum(forcas_normais) * (-1), sum(forcas_momento)/100], [sum(forcas_normais_2023) * (-1), sum(forcas_momento_2023)/100]

def calc_limite_4_4a(bx_indicado, bitola_aco, posicao_xy_barras, mod_elasticidade, fyd, fcd, dim_xy, ecu, ec2, coef_n, comp_secao, area_concreto_por_passo, lista_areas_aco_para_subtracao, fck):
    bx = bx_indicado
    bitola_cm = bitola_aco / 10   #cm
    pos_barras = posicao_xy_barras
    modulo_elasticidade = mod_elasticidade / 10   #kn/cm²
    fyd_cm = fyd / 10   #kn/cm²
    fcd_cm = fcd / 10   #kn/cm²
    cg = dim_xy / 2
    def_max_concreto = ecu
    forcas_normais = []
    forcas_momento = []
    forcas_normais_2023 = []
    forcas_momento_2023 = []
    forca_normal_concreto, forca_momento_concreto, forca_normal_concreto_2023, forca_momento_concreto_2023 = forca_concreto_total(posicao_xy_barras, bitola_aco, bx, def_max_concreto, comp_secao, ec2, fcd, coef_n, area_concreto_por_passo, cg, lista_areas_aco_para_subtracao, fck)
    forcas_normais.append(forca_normal_concreto)
    forcas_momento.append(forca_momento_concreto)
    forcas_normais_2023.append(forca_normal_concreto_2023)
    forcas_momento_2023.append(forca_momento_concreto_2023)

    for barra in pos_barras:
        area_de_aco = ((bitola_cm / 2) ** 2) * pi

        if barra < bx:
            deslocamento_barra = (bx - barra) * ecu / bx
        else:
            deslocamento_barra = (barra - bx) * ecu / bx

        tensao_tracao_aco = deslocamento_barra * modulo_elasticidade
        if tensao_tracao_aco > fyd_cm:
            tensao_tracao_aco = fyd_cm

        if barra < bx:
            forca_normal_aco = tensao_tracao_aco * area_de_aco
            forcas_normais.append(forca_normal_aco)
            forcas_normais_2023.append(forca_normal_aco)
            momento = forca_normal_aco * (cg - barra)
            forcas_momento.append(momento)
            forcas_momento_2023.append(momento)

        else:
            forca_normal_aco = tensao_tracao_aco * area_de_aco * (-1)
            forcas_normais.append(forca_normal_aco)
            forcas_normais_2023.append(forca_normal_aco)
            momento = forca_normal_aco * (cg - barra)
            forcas_momento.append(momento)
            forcas_momento_2023.append(momento)

    return [sum(forcas_normais) * (-1), sum(forcas_momento)/100], [sum(forcas_normais_2023) * (-1), sum(forcas_momento_2023)/100]

def calc_limite_4a_5_comp_max(bx_indicado, bitola_aco, posicao_xy_barras, mod_elasticidade, fyd, fcd, dim_xy, ecu, ec2, coef_n, comp_secao, area_concreto_por_passo, lista_areas_aco_para_subtracao, fck):
    bx = bx_indicado
    bitola_cm = bitola_aco / 10   #cm
    ponto_rotacao = (ecu - ec2) / ecu * dim_xy
    pos_barras = posicao_xy_barras
    modulo_elasticidade = mod_elasticidade / 10   #kn/cm²
    fyd_cm = fyd / 10   #kn/cm²
    fcd_cm = fcd / 10   #kn/cm²
    cg = dim_xy / 2
    forcas_normais = []
    forcas_momento = []
    forcas_normais_2023 = []
    forcas_momento_2023 = []
    ecu_calculos_compressao = ecu
    if ecu != ec2:
        ecu_calculos_compressao = bx * ec2 / (bx - ponto_rotacao)
    
    forca_normal_concreto, forca_momento_concreto, forca_normal_concreto_2023, forca_momento_concreto_2023 = forca_concreto_total(posicao_xy_barras, bitola_aco, bx, ecu_calculos_compressao, comp_secao, ec2, fcd, coef_n, area_concreto_por_passo, cg, lista_areas_aco_para_subtracao, fck)
    forcas_normais.append(forca_normal_concreto)
    forcas_momento.append(forca_momento_concreto)
    forcas_normais_2023.append(forca_normal_concreto_2023)
    forcas_momento_2023.append(forca_momento_concreto_2023)

    for barra in pos_barras:
        area_de_aco = ((bitola_cm / 2) ** 2) * pi
        deslocamento_barra = (bx - barra) * ecu_calculos_compressao / bx
        tensao_tracao_aco = deslocamento_barra * modulo_elasticidade
        if tensao_tracao_aco > fyd_cm:
            tensao_tracao_aco = fyd_cm

        if barra < bx:
            forca_normal_aco = tensao_tracao_aco * area_de_aco
            forcas_normais.append(forca_normal_aco)
            forcas_normais_2023.append(forca_normal_aco)
            momento = forca_normal_aco * (cg - barra)
            forcas_momento.append(momento)
            forcas_momento_2023.append(momento)

        else:
            forca_normal_aco = tensao_tracao_aco * area_de_aco * (-1)
            forcas_normais.append(forca_normal_aco)
            forcas_normais_2023.append(forca_normal_aco)
            momento = forca_normal_aco * (cg - barra)
            forcas_momento.append(momento)
            forcas_momento_2023.append(momento)

    return [sum(forcas_normais) * (-1), sum(forcas_momento)/100], [sum(forcas_normais_2023) * (-1), sum(forcas_momento_2023)/100]

def compressao_max(ec2, dim_x, dim_y, bitola_aco, quant_bitolas, fcd, coef_n, mod_elasticidade, fyd, fck):
    bitola = bitola_aco / 10   #cm
    fcd_cm = fcd / 10   #kn/cm²
    fyd_cm = fyd / 10   #kn/cm²
    modulo_elasticidade = mod_elasticidade / 10   #kn/cm²
    area_de_aco = ((bitola / 2) ** 2) * pi * quant_bitolas
    area_concreto = (dim_x * dim_y) - area_de_aco

    tensao_aco = ec2 * modulo_elasticidade
    if tensao_aco > fyd_cm:
        tensao_aco = fyd_cm
    tensao_compressao_concreto = tensao_concreto(ec2, ec2, fcd_cm, coef_n)
    tensao_compressao_concreto_2023 = tensao_concreto_2023(fck, ec2, ec2, fcd_cm, coef_n)

    forca_normal_concreto = tensao_compressao_concreto * area_concreto
    forca_normal_concreto_2023 = tensao_compressao_concreto_2023 * area_concreto
    forca_normal_aco = tensao_aco * area_de_aco
    forca_normal_total = forca_normal_concreto + forca_normal_aco
    forca_normal_total_2023 = forca_normal_concreto_2023 + forca_normal_aco

    return [(-1) * forca_normal_total, 0], [(-1) * forca_normal_total_2023, 0]

def pontos_bx(pontos_limites):
    limites = pontos_limites
    lista = []
    passo = 0.1
    i = limites[0]

    for bx in limites:
        if round(bx, 1) > bx:
            lista.append(round(bx, 1))
    lista.append(limites[0])

    if limites[0] > limites[1]:
        i = limites[1]
        lista.remove(limites[0])

    i = i // 1
    if i < limites[0]:
        i += 1
    while i <= limites[-1]:
        lista.append(round(i,2))
        if i > limites[-2]:
            i += 250
        else:
            i += passo

    lista.sort()
    return lista
    
def pontos_diagrama(sentido, hx, hy, posicao_barras_x, posicao_barras_y, area_passo_concreto_x, area_passo_concreto_y, es, fyd, bitola_aco, mod_elasticidade, ec2, fcd, coef_n, areas_bitola_por_passo, fck, ecu, numero_bitolas, posicao_primeira_barra_x, posicao_ultima_barra_x, d_linha, posicao_primeira_barra_y, posicao_ultima_barra_y):
    limites = limites_estados_deformacao(sentido, posicao_primeira_barra_x, posicao_ultima_barra_x, fyd, mod_elasticidade, es, ec2, ecu, d_linha, hx, hy, posicao_primeira_barra_y, posicao_ultima_barra_y)
    lista_bx = pontos_bx(limites)
    lista_pontos_diagrama = []
    lista_reversa = []
    lista_pontos_diagrama_2023 = []
    lista_reversa_2023 = []
    comp_secao = hx
    pos_barras = posicao_barras_x
    larg_secao = hy
    area_concreto_por_passo = area_passo_concreto_x
    aux_limites = copy.deepcopy(limites)

    del aux_limites[-1]

    if sentido == 'y':
        comp_secao = hy
        pos_barras = posicao_barras_y
        larg_secao = hx
        area_concreto_por_passo = area_passo_concreto_y

    for item in lista_bx:
        if limites[0] <= item <= limites[1]:
            ponto, ponto_2023 = calc_limite_tracaomax_1(item, pos_barras, comp_secao, es, fyd, bitola_aco, mod_elasticidade)
            ponto_inverso = [ponto[0], (-1)*ponto[1]]
            ponto_inverso_2023 = [ponto_2023[0], (-1)*ponto_2023[1]]

        elif limites[1] < item <= limites[2]:
            ponto, ponto_2023 = calc_limite_1_2(item, pos_barras, bitola_aco, ec2, es, mod_elasticidade, fyd, comp_secao, fcd, coef_n, comp_secao, area_concreto_por_passo, areas_bitola_por_passo, fck)
            ponto_inverso = [ponto[0], (-1)*ponto[1]]
            ponto_inverso_2023 = [ponto_2023[0], (-1)*ponto_2023[1]]
            
        elif limites[2] < item <= limites[3]:
            ponto, ponto_2023 = calc_limite_2_3(item, bitola_aco, pos_barras, mod_elasticidade, fyd, fcd, comp_secao, ecu, ec2, coef_n, comp_secao, area_concreto_por_passo, areas_bitola_por_passo, fck)
            ponto_inverso = [ponto[0], (-1)*ponto[1]]
            ponto_inverso_2023 = [ponto_2023[0], (-1)*ponto_2023[1]]

        elif limites[3] < item <= limites[4]:
            ponto, ponto_2023 = calc_limite_3_4(item, bitola_aco, pos_barras, mod_elasticidade, fyd, fcd, comp_secao, ecu, ec2, coef_n, comp_secao, area_concreto_por_passo, areas_bitola_por_passo, fck)
            ponto_inverso = [ponto[0], (-1)*ponto[1] ]
            ponto_inverso_2023 = [ponto_2023[0], (-1)*ponto_2023[1]]

        elif limites[4] < item <= limites[5]:
            ponto, ponto_2023 = calc_limite_4_4a(item, bitola_aco, pos_barras, mod_elasticidade, fyd, fcd, comp_secao, ecu, ec2, coef_n, comp_secao, area_concreto_por_passo, areas_bitola_por_passo, fck)
            ponto_inverso = [ponto[0], (-1)*ponto[1] ]
            ponto_inverso_2023 = [ponto_2023[0], (-1)*ponto_2023[1]]

        else:
            ponto, ponto_2023 = calc_limite_4a_5_comp_max(item, bitola_aco, pos_barras, mod_elasticidade, fyd, fcd, comp_secao, ecu, ec2, coef_n, comp_secao, area_concreto_por_passo, areas_bitola_por_passo, fck)
            ponto_inverso = [ponto[0], (-1)*ponto[1] ]
            ponto_inverso_2023 = [ponto_2023[0], (-1)*ponto_2023[1]]

        lista_pontos_diagrama.append(ponto)
        lista_reversa.append(ponto_inverso)
        lista_pontos_diagrama_2023.append(ponto_2023)
        lista_reversa_2023.append(ponto_inverso_2023)

    ponto, ponto_2023 = compressao_max(ec2, comp_secao, larg_secao, bitola_aco, numero_bitolas, fcd, coef_n, mod_elasticidade, fyd, fck)
    lista_pontos_diagrama.append(ponto)
    lista_pontos_diagrama_2023.append(ponto_2023)
    lista_reversa.reverse()
    lista_reversa_2023.reverse()
    lista_final = lista_pontos_diagrama + lista_reversa
    lista_final_2023 = lista_pontos_diagrama_2023 + lista_reversa_2023

    return lista_final, lista_final_2023

def limites_estados_deformacao(sentido, posicao_primeira_barra_x, posicao_ultima_barra_x, fyd, mod_elasticidade, es, ec2, ecu, d_linha, hx, hy, posicao_primeira_barra_y, posicao_ultima_barra_y):
    if sentido == 'x':
        limite_tracao_max_pilar = limite_tracao_max(posicao_primeira_barra_x, posicao_ultima_barra_x, fyd, mod_elasticidade, es)
        limite_1_pilar = limite_1()
        limite_2_pilar = limite_2(ecu, es, posicao_ultima_barra_x)
        limite_3_pilar = limite_3(ecu, fyd, mod_elasticidade, posicao_ultima_barra_x)
        limite_4_pilar = limite_4(ecu, posicao_ultima_barra_x)
        limite_4a_pilar = limite_4a(hx, d_linha, posicao_ultima_barra_x)
        limite_5_pilar = limite_5(ec2, ecu, hx)

    else:
        limite_tracao_max_pilar = limite_tracao_max(posicao_primeira_barra_y, posicao_ultima_barra_y, fyd, mod_elasticidade, es)
        limite_1_pilar = limite_1()
        limite_2_pilar = limite_2(ecu, es, posicao_ultima_barra_y)
        limite_3_pilar = limite_3(ecu, fyd, mod_elasticidade, posicao_ultima_barra_y)
        limite_4_pilar = limite_4(ecu, posicao_ultima_barra_y)
        limite_4a_pilar = round((limite_4a(hy, d_linha, posicao_ultima_barra_y)),2)
        limite_5_pilar = limite_5(ec2, ecu, hy)

    if limite_tracao_max_pilar > limite_1_pilar:
        limite_tracao_max_pilar = limite_1_pilar

    return [limite_tracao_max_pilar, limite_1_pilar, limite_2_pilar,
            limite_3_pilar, limite_4_pilar, limite_4a_pilar, limite_5_pilar]