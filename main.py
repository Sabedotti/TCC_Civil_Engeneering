import os
from math import pi as pi
from tkinter import Button, Entry, Frame, Label, PhotoImage, Tk
from tkinter.ttk import Combobox

from calculos import (area_por_passo_concreto, areas_de_concreto, calculo_fcd,
                      calculo_fyd, coordenadas_xy_barras_aco,
                      determinacao_coef_eta_c, diagrama_tensao_deformacao_aco,
                      diagrama_tensao_deformacao_concreto,
                      diagrama_tensao_deformacao_concreto_2023, ec2_ecu,
                      pontos_diagrama, posicionamento_das_barras,
                      subtracao_area_aco_bitola, tensao_concreto,
                      tensao_concreto_2023, valor_n)
from desenhos import desenho_secao_transversal_pilar
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from verificacoes import espacamentos_entre_barras, mensagens_consideracoes_st

caminho_arquivo = os.path.dirname(__file__)


class Pilar():
    def __init__(self):
        self.hx = 20.0   #
        self.hy = 20.0   #
        self.fck = 25.0   #
        self.gama_c = 1.4   #
        self.fyk = 500.0   #
        self.gama_s = 1.15   #
        self.mod_elasticidade = 210000.0   #
        self.d_linha = 5.0   #
        self.nx = 2.0   #
        self.ny = 2.0   #
        self.bitola_aco = 20.0   #
        self.posicao_barras = posicionamento_das_barras(
            self.hx, self.hy, self.nx, self.ny, self.d_linha)   #
        self.numero_bitolas = len(self.posicao_barras)   #
        self.posicao_barras_x, self.posicao_barras_y = \
            coordenadas_xy_barras_aco(self.posicao_barras)   #
        self.posicao_primeira_barra_x = min(self.posicao_barras_x)   #
        self.posicao_ultima_barra_x = max(self.posicao_barras_x)   #
        self.posicao_primeira_barra_y = min(self.posicao_barras_y)   #
        self.posicao_ultima_barra_y = max(self.posicao_barras_y)   #
        self.sentido_x = 'x'   #
        self.sentido_y = 'y'   #
        self.es = 10 / 1000   #
        self.ec2, self.ecu = ec2_ecu(self.fck)   #
        self.coef_n = valor_n(self.fck)   #
        self.taxa_armadura = 0.0   #
        self.area_concreto = 0.0   #
        self.area_aco = 0.0   #
        self.fcd = 0.0   #
        self.fyd = 0.0   #
        self.eta_c = 0.0   #
        self.area_passo_concreto_x = 0.0
        self.area_passo_concreto_y = 0.0
        self.areas_bitola_por_passo = []
        self.lista_pontos_dnmx_2014 = []
        self.lista_pontos_dnmy_2014 = []
        self.lista_pontos_dnmx_2023 = []
        self.lista_pontos_dnmy_2023 = []
        self.lista_pontos_mx_x_2014 = []
        self.lista_pontos_mx_y_2014 = []
        self.lista_pontos_mx_x_2023 = []
        self.lista_pontos_mx_y_2023 = []
        self.lista_pontos_my_x_2014 = []
        self.lista_pontos_my_y_2014 = []
        self.lista_pontos_my_x_2023 = []
        self.lista_pontos_my_y_2023 = []
        self.figura_diagrama = Figure(figsize=(10.9, 8.95), dpi=60)
        self.axes_dnm = self.figura_diagrama.add_subplot()
        self.eixo_zero_vertical_dnm, = self.axes_dnm.plot(
            [0, 0], [-1000000, 1000000], color='black', linewidth=1)
        self.eixo_zero_horizontal_dnm, = self.axes_dnm.plot(
            [-1000000, 1000000], [0, 0], color='black', linewidth=1)
        self.pontos_dnm, = self.axes_dnm.plot(
            [0, 0], [0, 0], color='blue', label='ABNT NBR 6118:2014')
        self.pontos_dnm_1, = self.axes_dnm.plot(
            [0, 0], [0, 0], color='red', label='ABNT NBR 6118:2023')
        self.espacamento_entre_barras_x = 0.0
        self.espacamento_entre_barras_y = 0.0
        self.diam_agregado_graudo = 1.9
        self.pontos_tracao_max = []
        self.areas_concreto_x = []
        self.areas_concreto_y = []


p1 = Pilar()


class ErrosEConsideracoes():
    def __init__(self, master):
        fonte = 'arial'
        self.tela = master
        self.container1 = Frame(self.tela, height=180, width=1000)
        self.container1.place(x=0, y=30)

        self.container2 = Frame(self.tela, height=440, width=1000)
        self.container2.place(x=0, y=210)

        self.title_erros_consideracoes = Label(
            self.tela, text='Considerações Sobre a Seção Transversal '
            'Informada', font=('arial', 16, 'bold'))
        self.title_erros_consideracoes.place(x=190, y=0)

        self.lbl_dados_selecionados = Label(
            self.container1, text='Informações da Seção Transversal',
            font=('arial', 14, 'bold'))
        self.lbl_dados_selecionados.place(x=300, y=0)

        self.lbl_hx = Label(
            self.container1, text=f'Dimensão x: {p1.hx} cm',
            font=('arial', 12))
        self.lbl_hx.place(x=20, y=30)

        self.lbl_hy = Label(
            self.container1, text=f'Dimensão y: {p1.hy} cm',
            font=('arial', 12))
        self.lbl_hy.place(x=20, y=50)

        self.lbl_nx = Label(
            self.container1, text=f'Número de barras no sentido x: {p1.nx} '
            'barras', font=('arial', 12))
        self.lbl_nx.place(x=20, y=70)

        self.lbl_ny = Label(
            self.container1, text=f'Número de barras no sentido y: {p1.ny} '
            'barras', font=('arial', 12))
        self.lbl_ny.place(x=20, y=90)

        self.lbl_dlinha = Label(
            self.container1, text=f"Espaçamento d': {p1.d_linha} cm",
            font=('arial', 12))
        self.lbl_dlinha.place(x=20, y=110)

        self.lbl_bitola = Label(
            self.container1, text=f'Bitola de aço: {p1.bitola_aco} mm',
            font=('arial', 12))
        self.lbl_bitola.place(x=20, y=130)

        self.lbl_agregado = Label(
            self.container1, text='Diâmetro Característica do Agregado '
            f'Graúdo Considerado: {p1.diam_agregado_graudo} cm',
            font=('arial', 12))
        self.lbl_agregado.place(x=20, y=150)

        lista_verificacoes = mensagens_consideracoes_st(
            p1.hx, p1.hy, p1.area_aco, p1.espacamento_entre_barras_x,
            p1.espacamento_entre_barras_y, p1.bitola_aco,
            p1.diam_agregado_graudo)

        self.lbl_consideracoes = Label(
            self.container2, text='Considerações Normativas',
            font=(fonte, 14, 'bold'))
        self.lbl_consideracoes.place(x=350, y=0)

        self.lbl_disp_gerais = Label(
            self.container2, text='Disposições Gerais',
            font=(fonte, 12, 'bold'), foreground='black')
        self.lbl_disp_gerais.place(x=20, y=20)

        self.lbl_verif_1 = Label(
            self.container2, text=lista_verificacoes[0][1],
            foreground='red', font=(fonte, 12))
        if lista_verificacoes[0][0] == 0:
            self.lbl_verif_1['foreground'] = 'green'
        self.lbl_verif_1.place(x=20, y=45)

        self.lbl_verif_2 = Label(
            self.container2, text=lista_verificacoes[1][1][0:123],
            foreground='red', font=(fonte, 12))
        if lista_verificacoes[1][0] == 0:
            self.lbl_verif_2['foreground'] = 'green'
        self.lbl_verif_2.place(x=20, y=70)

        self.lbl_verif_2_1 = Label(
            self.container2, text=lista_verificacoes[1][1][124:],
            foreground='red', font=(fonte, 12))
        if lista_verificacoes[1][0] == 0:
            self.lbl_verif_2_1['foreground'] = 'green'
        self.lbl_verif_2_1.place(x=20, y=90)

        self.areas_de_aço = Label(
            self.container2, text='Áreas de Aço', font=(fonte, 12, 'bold'),
            foreground='black')
        self.areas_de_aço.place(x=20, y=130)

        self.lbl_verif_3 = Label(
            self.container2, text=lista_verificacoes[2][1], foreground='black',
            font=(fonte, 12))
        self.lbl_verif_3.place(x=20, y=155)

        self.lbl_verif_4 = Label(
            self.container2, text=lista_verificacoes[3][1], foreground='red',
            font=(fonte, 12))
        if lista_verificacoes[3][0] == 0:
            self.lbl_verif_4['foreground'] = 'green'
        self.lbl_verif_4.place(x=20, y=180)

        self.lbl_verif_5 = Label(
            self.container2, text=lista_verificacoes[4][1][0:128],
            foreground='black', font=(fonte, 12))
        self.lbl_verif_5.place(x=20, y=205)

        self.lbl_verif_5_1 = Label(
            self.container2, text=lista_verificacoes[4][1][128:],
            foreground='black', font=(fonte, 12))
        self.lbl_verif_5_1.place(x=20, y=225)

        self.lbl_verif_6 = Label(
            self.container2, text=lista_verificacoes[5][1], foreground='red',
            font=(fonte, 12))
        if lista_verificacoes[5][0] == 0:
            self.lbl_verif_6['foreground'] = 'green'
        self.lbl_verif_6.place(x=20, y=250)

        self.lbl_espacamentos = Label(
            self.container2, text="Espacamentos e Dimensões das Bitolas",
            font=(fonte, 12, 'bold'), foreground='black')
        self.lbl_espacamentos.place(x=20, y=290)

        self.lbl_verif_7 = Label(
            self.container2, text=lista_verificacoes[6][1], foreground='red',
            font=(fonte, 12))
        if lista_verificacoes[6][0] == 0:
            self.lbl_verif_7['foreground'] = 'green'
        self.lbl_verif_7.place(x=20, y=315)

        self.lbl_verif_8 = Label(
            self.container2, text=lista_verificacoes[7][1], foreground='red',
            font=(fonte, 12))
        if lista_verificacoes[7][0] == 0:
            self.lbl_verif_8['foreground'] = 'green'
        self.lbl_verif_8.place(x=20, y=340)

        self.lbl_verif_9 = Label(
            self.container2, text=lista_verificacoes[8][1], foreground='red',
            font=(fonte, 12))
        if lista_verificacoes[8][0] == 0:
            self.lbl_verif_9['foreground'] = 'green'
        self.lbl_verif_9.place(x=20, y=365)

        self.lbl_verif_10 = Label(
            self.container2, text=lista_verificacoes[9][1], foreground='red',
            font=(fonte, 12))
        if lista_verificacoes[9][0] == 0:
            self.lbl_verif_10['foreground'] = 'green'
        self.lbl_verif_10.place(x=20, y=390)

        self.lbl_verif_11 = Label(
            self.container2, text=lista_verificacoes[10][1], foreground='red',
            font=(fonte, 12))
        if lista_verificacoes[10][0] == 0:
            self.lbl_verif_11['foreground'] = 'green'
        self.lbl_verif_11.place(x=20, y=415)


class TelaDiagramasTensaoDeformacao():
    def __init__(self, master):
        self.tela = master
        self.container1 = Frame(
            self.tela, height=340, width=1000, highlightbackground='black',
            highlightthickness=1)
        self.container1.place(x=0, y=0)

        self.container2 = Frame(
            self.tela, height=340, width=1000, highlightbackground='black',
            highlightthickness=1)
        self.container2.place(x=0, y=340)

        self.container1_1 = Frame(
            self.container1, height=305, width=485,
            highlightbackground='black', highlightthickness=1)
        self.container1_1.place(x=10, y=30)

        self.container1_2 = Frame(
            self.container1, height=305, width=485,
            highlightbackground='black', highlightthickness=1)
        self.container1_2.place(x=505, y=30)

        self.container2_1 = Frame(
            self.container2, height=305, width=485,
            highlightbackground='black', highlightthickness=1)
        self.container2_1.place(x=10, y=30)

        self.container2_2 = Frame(
            self.container2, height=305, width=485,
            highlightbackground='black', highlightthickness=1)
        self.container2_2.place(x=505, y=30)

        self.title_dtd_concreto = Label(
            self.container1,
            text='Diagrama Tensão x Deformação para o Concreto',
            font=('arial', 16, 'bold'))
        self.title_dtd_concreto.place(x=255, y=0)

        self.title_dtd_aco = Label(
            self.container2,
            text='Diagrama Tensão x Deformação para o Aço',
            font=('arial', 16, 'bold'))
        self.title_dtd_aco.place(x=270, y=0)

        # Diagramas Tensão x Deformação dos Materiais
        eixo_x_dtd_concreto_2014, eixo_y_dtd_concreto_2014 = \
            diagrama_tensao_deformacao_concreto(
                p1.ec2, p1.ecu, p1.fck, p1.gama_c)

        eixo_x_dtd_concreto_2023, eixo_y_dtd_concreto_2023 = \
            diagrama_tensao_deformacao_concreto_2023(
                p1.ec2, p1.ecu, p1.fck, p1.gama_c)
        figura_1 = Figure(figsize=(8.03, 4.35), dpi=60)
        self.desenho_diagrama_1 = FigureCanvasTkAgg(
            figura_1, self.container1_2)
        NavigationToolbar2Tk(self.desenho_diagrama_1, self.container1_2)
        axes_1 = figura_1.add_subplot()
        tensao_ec2_2014 = tensao_concreto(p1.ec2, p1.ec2, p1.fcd, p1.coef_n)
        tensao_ecu_2014 = tensao_concreto(p1.ecu, p1.ec2, p1.fcd, p1.coef_n)
        tensao_ec2_2023 = tensao_concreto_2023(
            p1.fck, p1.ec2, p1.ec2, p1.fcd, p1.coef_n)
        tensao_ecu_2023 = tensao_concreto_2023(
            p1.fck, p1.ecu, p1.ec2, p1.fcd, p1.coef_n)
        axes_1.set_title(
            f'Diagrama Tensão x Deformação Concreto C{int(p1.fck)}')
        axes_1.plot(eixo_x_dtd_concreto_2014, eixo_y_dtd_concreto_2014,
                    label='ABNT NBR 6118:2014', color='blue')
        axes_1.plot(p1.ec2*1000, tensao_ec2_2014/10,
                    label=f'εc2: {round(p1.ec2*1000, 3)}‰ , '
                    f'σ: {round(tensao_ec2_2014/10, 3)} kN/cm²',
                    marker='x', color='blue')
        axes_1.plot(p1.ecu*1000, tensao_ecu_2014/10,
                    label=f'εcu: {round(p1.ecu*1000, 3)}‰ , '
                    f'σ: {round(tensao_ecu_2014/10, 3)} kN/cm²',
                    marker='o', color='blue')
        axes_1.plot(eixo_x_dtd_concreto_2023, eixo_y_dtd_concreto_2023,
                    ls='--', label='ABNT NBR 6118:2023', color='red')
        axes_1.plot(p1.ec2*1000, tensao_ec2_2023/10,
                    label=f'εc2: {round(p1.ec2*1000, 3)}‰ , '
                    f'σ: {round(tensao_ec2_2023/10, 3)} kN/cm²',
                    marker='x', color='red')
        axes_1.plot(p1.ecu*1000, tensao_ecu_2023/10,
                    label=f'εcu: {round(p1.ecu*1000, 3)}‰ , '
                    f'σ: {round(tensao_ecu_2023/10, 3)} kN/cm²',
                    marker='o', color='red')
        axes_1.set_ylabel('Tensão (kN/cm²)')
        axes_1.set_xlabel('Deformação (‰)')
        axes_1.grid(True, 'both', 'both')
        axes_1.legend(loc='lower right')
        axes_1.set_xlim(0, max(eixo_x_dtd_concreto_2014) + 0.2)
        axes_1.set_ylim(0, max(eixo_y_dtd_concreto_2014) + 0.2)

        self.desenho_diagrama_1.get_tk_widget().pack()

        eixo_x_dtd_aco, eixo_y_dtd_aco = diagrama_tensao_deformacao_aco(
            p1.fyd, p1.es, p1.ecu, p1.mod_elasticidade)
        figura_2 = Figure(figsize=(8.03, 4.35), dpi=60)
        self.desenho_diagrama_2 = FigureCanvasTkAgg(
            figura_2, self.container2_2)
        NavigationToolbar2Tk(self.desenho_diagrama_2, self.container2_2)
        axes_2 = figura_2.add_subplot()
        axes_2.plot(eixo_x_dtd_aco, eixo_y_dtd_aco,
                    label='Ambas as Normas', color='green')
        axes_2.plot([0, 0], [-1000, 1000], color='black', linewidth=1)
        axes_2.plot([-1000, 1000], [0, 0], color='black', linewidth=1)
        axes_2.set_title(
            f'Diagrama Tensão x Deformação Aço CA-{int(p1.fyk/10)}, para '
            f'Concreto C{int(p1.fck)}')
        axes_2.set_xlim(min(eixo_x_dtd_aco) - 0.5, max(eixo_x_dtd_aco) + 0.5)
        axes_2.plot(p1.fyd/p1.mod_elasticidade*1000, p1.fyd/10,
                    label=f'εyd: {round(p1.fyd/p1.mod_elasticidade*1000, 3)}‰,'
                    f' σ: {round(p1.fyd/10, 3)} kN/cm²',
                    color='green', marker='x', markersize=10)
        axes_2.plot(p1.fyd/p1.mod_elasticidade*(-1000), p1.fyd / (-10),
                    color='green', marker='x', markersize=10)
        axes_2.plot(p1.ecu*(-1000), p1.fyd/(-10),
                    label=f'εs Compressão: {round(p1.ecu*(-1000),3)} ‰, '
                    f'σ: {round(p1.fyd/(-10), 3)} kN/cm²',
                    color='green', marker='p', markersize=10)
        axes_2.plot(p1.es*1000, p1.fyd/(10),
                    label=f'εs Tração: {round(p1.es*1000,3)} ‰, '
                    f'σ: {round(p1.fyd/(10), 3)} kN/cm²',
                    color='green', marker='o', markersize=10)
        axes_2.set_ylim(min(eixo_y_dtd_aco) + (min(eixo_y_dtd_aco) * 0.1),
                        max(eixo_y_dtd_aco) + (max(eixo_y_dtd_aco) * 0.1))
        axes_2.set_ylabel('Tensão (kN/cm²)')
        axes_2.set_xlabel('Deformação (‰)')
        axes_2.grid(True, 'both', 'both')
        axes_2.legend(loc='lower right')

        self.desenho_diagrama_2.get_tk_widget().pack()

        # Dados dos Materiais
        self.title_dtd_concreto = Label(
            self.container1_1, text='Informações sobre o Concreto',
            font=('arial', 12, 'bold'))
        self.title_dtd_concreto.place(x=125, y=0)

        self.lbl_classe_concreto = Label(
            self.container1_1, text='Classe de Concreto Selecionada: '
            f'C{int(p1.fck)}', font=('arial', 12))
        self.lbl_classe_concreto.place(x=10, y=30)

        self.lbl_fck_concreto = Label(
            self.container1_1, text=f'fck: {p1.fck} MPa', font=('arial', 12))
        self.lbl_fck_concreto.place(x=330, y=30)

        self.lbl_coef_gama_c = Label(
            self.container1_1, text=f'Coeficiente γc: {p1.gama_c}',
            font=('arial', 12))
        self.lbl_coef_gama_c.place(x=10, y=60)

        self.lbl_fcd_concreto = Label(
            self.container1_1, text=f'fcd: {round(p1.fcd, 3)} MPa',
            font=('arial', 12))
        self.lbl_fcd_concreto.place(x=330, y=60)

        self.lbl_ec2_1 = Label(
            self.container1_1, text='Deformação Específica do Concreto',
            font=('arial', 12))
        self.lbl_ec2_1.place(x=10, y=90)

        self.lbl_ec2_2 = Label(
            self.container1_1, text='no Início do Patamar Plástico (εc2): ',
            font=('arial', 12))
        self.lbl_ec2_2.place(x=10, y=110)

        self.lbl_ec2_3 = Label(
            self.container1_1, text=f'{round(p1.ec2 * 1000, 3)} ‰',
            font=('arial', 12))
        self.lbl_ec2_3.place(x=275, y=100)

        self.lbl_ecu_1 = Label(
            self.container1_1, text='Deformação Específica do Concreto',
            font=('arial', 12))
        self.lbl_ecu_1.place(x=10, y=140)

        self.lbl_ecu_2 = Label(
            self.container1_1, text='na Ruptura (εcu): ', font=('arial', 12))
        self.lbl_ecu_2.place(x=10, y=160)

        self.lbl_ecu_3 = Label(
            self.container1_1, text=f'{round(p1.ecu * 1000, 3)} ‰',
            font=('arial', 12))
        self.lbl_ecu_3.place(x=275, y=150)

        self.lbl_coef_n = Label(
            self.container1_1, text=f'Coeficiente n: {round(p1.coef_n, 3)}',
            font=('arial', 12))
        self.lbl_coef_n.place(x=10, y=190)

        self.lbl_eta_c = Label(
            self.container1_1, text='Coeficiente de Fragilidade - ηc:',
            font=('arial', 12))
        self.lbl_eta_c.place(x=10, y=225)

        self.lbl_eta_c_2014 = Label(
            self.container1_1, text='ABNT NBR 6118:2014: Parâmetro não '
            'existente na norma', font=('arial', 12))
        self.lbl_eta_c_2014.place(x=40, y=245)

        self.lbl_eta_c_2023 = Label(
            self.container1_1, text='ABNT NBR 6118:2023: '
            f'ηc={round(p1.eta_c, 3)}', font=('arial', 12))
        self.lbl_eta_c_2023.place(x=40, y=265)

        # Informações Aço
        self.title_dtd_aco = Label(
            self.container2_1, text='Informações sobre o Aço',
            font=('arial', 12, 'bold'))
        self.title_dtd_aco.place(x=140, y=0)

        self.lbl_classe_aco = Label(
            self.container2_1, text='Classe de Aço Selecionada: '
            f'CA-{int(p1.fyk / 10)}', font=('arial', 12))
        self.lbl_classe_aco.place(x=10, y=30)

        self.lbl_fyk_aco = Label(
            self.container2_1, text=f'fyk: {p1.fyk} MPa', font=('arial', 12))
        self.lbl_fyk_aco.place(x=330, y=30)

        self.lbl_coef_gama_s = Label(
            self.container2_1, text=f'Coeficiente γs: {p1.gama_s}',
            font=('arial', 12))
        self.lbl_coef_gama_s.place(x=10, y=60)

        self.lbl_fyd_aco = Label(
            self.container2_1, text=f'fyd: {round(p1.fyd, 3)} MPa',
            font=('arial', 12))
        self.lbl_fyd_aco.place(x=330, y=60)

        self.lbl_mod_elast = Label(
            self.container2_1, text='Módulo de Elasticidade - '
            f'Es: {p1.mod_elasticidade} MPa', font=('arial', 12))
        self.lbl_mod_elast.place(x=10, y=90)

        self.lbl_es_1 = Label(
            self.container2_1, text='Máxima Deformação Específica do',
            font=('arial', 12))
        self.lbl_es_1.place(x=10, y=120)

        self.lbl_es_2 = Label(
            self.container2_1, text='Aço da Armadura Passiva (alongamento)  '
            '- εs:', font=('arial', 12))
        self.lbl_es_2.place(x=10, y=140)

        self.lbl_es_3 = Label(
            self.container2_1, text=f'{p1.es * 1000} ‰', font=('arial', 12))
        self.lbl_es_3.place(x=350, y=130)


class Aplication:
    def __init__(self, master):
        fonte = 'arial'
        lista_bitolas = ['5.0', '6.3', '8.0', '10.0',
                         '12.5', '16.0', '20.0', '25.0', '32.0', '40.0']
        classes_concreto_str = ['20', '25', '30', '35', '40', '45', '50', '55',
                                '60', '70', '80', '90']
        classes_concreto = [20, 25, 30, 35, 40, 45, 50, 55,
                            60, 70, 80, 90]
        anos_norma = ['2014', '2023', 'Ambos']
        sentido_diagrama_n_m = ['N x Mx', 'N x My']
        self.sentido_selecionado = ''
        self.norma_selecionada = ''

        # funções
        def tela_consideracoes_norma():
            tela_erros_e_consideracoes = Tk()
            tela_erros_e_consideracoes.title(
                'Considerações para Seção Transversal - '
                'Desenvolvido por João Paulo da Silva Sabedotti')
            tela_erros_e_consideracoes.geometry('1000x670+180+10')
            ErrosEConsideracoes(tela_erros_e_consideracoes)
            root.mainloop()

        def button_confirm_st():
            # Pegar Informações das Caixas de Texto
            i = 0
            self.lbl_erro_variaveis.config(text='', foreground='red')
            self.entry_dim_x.config(foreground='red')
            self.entry_dim_y.config(foreground='red')
            self.entry_nx.config(foreground='red')
            self.entry_ny.config(foreground='red')
            self.entry_dlinha.config(foreground='red')
            self.listbox_bitola.config(foreground='red')

            try:
                p1.hx = float(self.entry_dim_x.get())
                p1.hy = float(self.entry_dim_y.get())
                p1.nx = float(self.entry_nx.get())
                p1.ny = float(self.entry_ny.get())
                p1.d_linha = float(self.entry_dlinha.get())
                p1.bitola_aco = float(self.listbox_bitola.get())

            except Exception:
                self.lbl_erro_variaveis.config(
                    text='Insira os parâmetros corretamente', foreground='red')

            self.lbl_erro_variaveis.config(text='', foreground='red')
            self.entry_dim_x.config(foreground='green')
            self.entry_dim_y.config(foreground='green')
            self.entry_nx.config(foreground='green')
            self.entry_ny.config(foreground='green')
            self.entry_dlinha.config(foreground='green')
            self.listbox_bitola.config(foreground='green')

            # Verificações
            if p1.hx < 14:
                self.entry_dim_x.config(foreground='red')
                i = 1

            if p1.hy < 14:
                self.entry_dim_y.config(foreground='red')
                i = 1

            if (p1.hx * p1.hy) < 360:
                self.entry_dim_x.config(foreground='red')
                self.entry_dim_y.config(foreground='red')
                i = 1

            if p1.nx < 2:
                self.entry_nx.config(foreground='red')
                i = 1
            if p1.nx > ((p1.hx - (2 * p1.d_linha) + p1.bitola_aco/10) /
                        (p1.bitola_aco/10)):
                self.entry_nx.config(foreground='red')
                i = 1

            if p1.ny < 2:
                self.entry_ny.config(foreground='red')
                i = 1
            if p1.ny > ((p1.hy - (2 * p1.d_linha) + p1.bitola_aco/10) /
                        (p1.bitola_aco/10)):
                self.entry_ny.config(foreground='red')
                i = 1

            if p1.d_linha - (p1.bitola_aco/20) <= 0:
                self.entry_dlinha.config(foreground='red')
                i = 1

            elif p1.d_linha + (p1.bitola_aco/20) > p1.hx/2:
                self.entry_dlinha.config(foreground='red')
                i = 1

            elif p1.d_linha + (p1.bitola_aco/20) > p1.hy/2:
                self.entry_dlinha.config(foreground='red')
                i = 1

            else:
                self.entry_dlinha.config(foreground='green')

            if str(p1.bitola_aco) not in lista_bitolas:
                self.listbox_bitola.config(foreground='red')
                i = 1

            if i == 1:
                self.lbl_erro_variaveis.config(
                    text='Dados inseridos inconsistentes!')
                return

            p1.espacamento_entre_barras_x, p1.espacamento_entre_barras_y = \
                espacamentos_entre_barras(
                    p1.hx, p1.hy, p1.nx, p1.ny, p1.d_linha, p1.bitola_aco)
            p1.posicao_barras = posicionamento_das_barras(
                p1.hx, p1.hy, p1.nx, p1.ny, p1.d_linha)
            p1.numero_bitolas = len(p1.posicao_barras)
            p1.posicao_barras_x, p1.posicao_barras_y = \
                coordenadas_xy_barras_aco(p1.posicao_barras)
            p1.posicao_primeira_barra_x = min(p1.posicao_barras_x)
            p1.posicao_ultima_barra_x = max(p1.posicao_barras_x)
            p1.posicao_primeira_barra_y = min(p1.posicao_barras_y)
            p1.posicao_ultima_barra_y = max(p1.posicao_barras_y)
            p1.areas_concreto_x = areas_de_concreto(
                p1.posicao_barras_y, p1.hx, p1.hy, p1.bitola_aco)
            p1.areas_concreto_y = areas_de_concreto(
                p1.posicao_barras_y, p1.hy, p1.hx, p1.bitola_aco)
            p1.area_aco = ((p1.bitola_aco / 10 / 2) ** 2) * \
                pi * p1.numero_bitolas
            p1.area_concreto = (p1.hx * p1.hy)
            p1.taxa_armadura = round(
                (p1.area_aco / (p1.area_concreto) * 100), 3)
            p1.area_passo_concreto_x = area_por_passo_concreto(0.01, p1.hy)
            p1.area_passo_concreto_y = area_por_passo_concreto(0.01, p1.hx)
            p1.areas_bitola_por_passo = subtracao_area_aco_bitola(
                p1.bitola_aco)

            self.lbl_area_concreto.config(
                text=f'Área de Concreto: {p1.area_concreto} cm²')
            self.lbl_area_aco.config(
                text=f'Área de Aço: {round(p1.area_aco,3)} cm²')
            self.lbl_taxa_armadura.config(
                text=f'Taxa de Armadura: {p1.taxa_armadura}%')

            img = desenho_secao_transversal_pilar(
                p1.hx, p1.hy, p1.nx, p1.ny, p1.d_linha, p1.bitola_aco)
            img = PhotoImage(file='programa_tcc\\imagem_nova.png')
            self.lbl.image = img  # type: ignore
            self.lbl['image'] = img
            self.lbl_erro_variaveis.config(
                text='Dados inseridos estão OK!', foreground='green')

        def button_confirm_caract_mat():
            self.lbl_erro_materiais.config(text='', foreground='red')
            self.combobox_fck.config(foreground='red')
            self.entry_gama_c.config(foreground='red')
            self.entry_fyk.config(foreground='red')
            self.entry_mod_elast.config(foreground='red')
            self.entry_gama_s.config(foreground='red')
            i = 0

            try:
                p1.fck = float(self.combobox_fck.get())
                p1.fyk = float(self.entry_fyk.get())
                p1.mod_elasticidade = float(self.entry_mod_elast.get())
                p1.gama_c = float(self.entry_gama_c.get())
                p1.gama_s = float(self.entry_gama_s.get())

            except Exception:
                self.lbl_erro_materiais.config(
                    text='Variáveis não foram inseridas!', font=(fonte, 10))
                return

            self.combobox_fck.config(foreground='green')
            self.entry_gama_c.config(foreground='green')
            self.entry_fyk.config(foreground='green')
            self.entry_mod_elast.config(foreground='green')
            self.entry_gama_s.config(foreground='green')

            if p1.fck not in classes_concreto:
                self.combobox_fck.config(foreground='red')
                i = 1

            if p1.gama_c <= 0:
                self.entry_gama_c.config(foreground='red')
                i = 1

            if p1.fyk <= 0:
                self.entry_fyk.config(foreground='red')
                i = 1

            if p1.mod_elasticidade <= 0:
                self.entry_mod_elast.config(foreground='red')
                i = 1

            if p1.gama_s <= 0:
                self.entry_gama_s.config(foreground='red')
                i = 1

            if i == 1:
                self.lbl_erro_materiais.config(
                    text='Dados inseridos inconsistentes!')
                return

            p1.fcd = calculo_fcd(p1.fck, p1.gama_c)
            p1.fyd = calculo_fyd(p1.fyk, p1.gama_s)
            p1.ec2, p1.ecu = ec2_ecu(p1.fck)
            p1.coef_n = valor_n(p1.fck)
            p1.eta_c = determinacao_coef_eta_c(p1.fck)
            self.lbl_fcd_3.config(text=f'{round(p1.fcd, 3)} MPa')
            self.lbl_fyd_3.config(text=f'{round(p1.fyd, 3)} MPa')
            p1.posicao_primeira_barra_x = min(p1.posicao_barras_x)   #
            p1.posicao_ultima_barra_x = max(p1.posicao_barras_x)   #
            p1.posicao_primeira_barra_y = min(p1.posicao_barras_y)   #
            p1.posicao_ultima_barra_y = max(p1.posicao_barras_y)   #
            p1.lista_pontos_dnmx_2014, p1.lista_pontos_dnmx_2023 = \
                pontos_diagrama('y', p1.hx, p1.hy, p1.posicao_barras_x,
                                p1.posicao_barras_y, p1.area_passo_concreto_x,
                                p1.area_passo_concreto_y, p1.es, p1.fyd,
                                p1.bitola_aco, p1.mod_elasticidade, p1.ec2,
                                p1.fcd, p1.coef_n, p1.areas_bitola_por_passo,
                                p1.fck, p1.ecu, p1.numero_bitolas,
                                p1.posicao_primeira_barra_x,
                                p1.posicao_ultima_barra_x, p1.d_linha,
                                p1.posicao_primeira_barra_y,
                                p1.posicao_ultima_barra_y)
            p1.lista_pontos_dnmy_2014, p1.lista_pontos_dnmy_2023 = \
                pontos_diagrama('x', p1.hx, p1.hy, p1.posicao_barras_x,
                                p1.posicao_barras_y, p1.area_passo_concreto_x,
                                p1.area_passo_concreto_y, p1.es, p1.fyd,
                                p1.bitola_aco, p1.mod_elasticidade,
                                p1.ec2, p1.fcd, p1.coef_n,
                                p1.areas_bitola_por_passo, p1.fck, p1.ecu,
                                p1.numero_bitolas, p1.posicao_primeira_barra_x,
                                p1.posicao_ultima_barra_x, p1.d_linha,
                                p1.posicao_primeira_barra_y,
                                p1.posicao_ultima_barra_y)
            p1.lista_pontos_mx_x_2014 = []
            p1.lista_pontos_mx_y_2014 = []
            p1.lista_pontos_my_x_2014 = []
            p1.lista_pontos_my_y_2014 = []
            p1.lista_pontos_mx_x_2023 = []
            p1.lista_pontos_mx_y_2023 = []
            p1.lista_pontos_my_x_2023 = []
            p1.lista_pontos_my_y_2023 = []

            for item in p1.lista_pontos_dnmx_2014:
                p1.lista_pontos_mx_x_2014.append(item[1])
                p1.lista_pontos_mx_y_2014.append(item[0])

            for item in p1.lista_pontos_dnmy_2014:
                p1.lista_pontos_my_x_2014.append(item[1])
                p1.lista_pontos_my_y_2014.append(item[0])

            for item in p1.lista_pontos_dnmx_2023:
                p1.lista_pontos_mx_x_2023.append(item[1])
                p1.lista_pontos_mx_y_2023.append(item[0])

            for item in p1.lista_pontos_dnmy_2023:
                p1.lista_pontos_my_x_2023.append(item[1])
                p1.lista_pontos_my_y_2023.append(item[0])

            self.lbl_erro_materiais.config(
                text='Dados Gerados com Sucesso', foreground='green')

        def gerar_diagrama_n_m():
            self.sentido_selecionado = self.combobox_sentido.get()
            self.norma_selecionada = self.combobox_norma.get()
            p1.axes_dnm.clear()
            p1.axes_dnm.grid(True, 'both', 'both')
            p1.axes_dnm.set_ylabel('Força Normal (kN)')
            p1.axes_dnm.set_xlabel('Momento (kN*m)')
            p1.axes_dnm.plot([0, 0], [-500000, 500000],
                             color='black', linewidth=1)
            p1.axes_dnm.plot([-500000, 500000], [0, 0],
                             color='black', linewidth=1)

            if str(self.sentido_selecionado) not in sentido_diagrama_n_m:
                self.lbl_erro_geracao_diagrama.config(
                    text='Favor verificar o item "Sentido do Diagrama"!',
                    foreground='red')
                return
            # escrevi aqui
            elif str(self.norma_selecionada) not in anos_norma:
                self.lbl_erro_geracao_diagrama.config(
                    text='Favor verificar o item "Norma"!', foreground='red')
                return

            elif p1.lista_pontos_dnmx_2014 == []:
                self.lbl_erro_geracao_diagrama.config(
                    text='Faltam informações para gerar o diagrama!',
                    foreground='red')

            elif p1.taxa_armadura == ' - ':
                self.lbl_erro_geracao_diagrama.config(
                    text='Faltam informações para gerar o diagrama',
                    foreground='red')

            else:
                lista_x = []
                lista_y = []
                lista_x_ambas = []
                lista_y_ambas = []
                self.lbl_erro_geracao_diagrama.config(
                    text='Diagrama gerado com sucesso!', foreground='green')

                if self.sentido_selecionado == 'N x Mx':
                    p1.axes_dnm.set_title(
                        'Diagrama de Interação N-Mx (FCN)', fontsize=26)
                    if self.norma_selecionada == '2014':
                        lista_x = p1.lista_pontos_mx_x_2014
                        lista_y = p1.lista_pontos_mx_y_2014
                        ponto_compressao_maximo = min(lista_y)
                        ponto_tracao_maximo = max(lista_y)
                        momento_max_x = max(lista_x)
                        momento_min_x = momento_max_x * (-1)
                        index_momento_max = lista_x.index(momento_max_x)
                        momento_max_y = lista_y[index_momento_max]
                        p1.axes_dnm.plot(
                            lista_x, lista_y, color='blue',
                            label='ABNT NBR 6118:2014')
                        p1.pontos_tracao_max = p1.axes_dnm.plot(
                            0, ponto_tracao_maximo, marker='p',
                            markersize=10, color='blue',
                            label=f'Nmax (tração)= '
                            f'{round(ponto_tracao_maximo, 2)} kN')
                        p1.axes_dnm.plot(
                            0, ponto_compressao_maximo, marker='o',
                            markersize=10, color='blue',
                            label=f'Nmin (compressão)= '
                            f'{round(ponto_compressao_maximo, 2)} kN')
                        p1.axes_dnm.plot(
                            momento_max_x, momento_max_y, marker='x',
                            markersize=10, color='blue',
                            label=f'Mmax= {round(momento_max_x, 2)} kN*m, '
                            f'N={round(momento_max_y,2)} kN')
                        p1.axes_dnm.plot(
                            momento_min_x, momento_max_y, marker='x',
                            markersize=10, color='blue')

                    elif self.norma_selecionada == '2023':
                        lista_x = p1.lista_pontos_mx_x_2023
                        lista_y = p1.lista_pontos_mx_y_2023
                        p1.axes_dnm.plot(
                            lista_x, lista_y, color='red',
                            label='ABNT NBR 6118:2023')
                        ponto_tracao_maximo = max(lista_y)
                        ponto_compressao_maximo = min(lista_y)
                        momento_max_x = max(lista_x)
                        index_momento_max = lista_x.index(momento_max_x)
                        momento_max_y = lista_y[index_momento_max]
                        p1.pontos_tracao_max = p1.axes_dnm.plot(
                            0, ponto_tracao_maximo, marker='p',
                            markersize=10, color='red',
                            label='Nmax (tração)= '
                            f'{round(ponto_tracao_maximo, 2)} kN')
                        p1.axes_dnm.plot(
                            0, ponto_compressao_maximo, marker='o',
                            markersize=10, color='red',
                            label='Nmin (compressão)= '
                            f'{round(ponto_compressao_maximo, 2)} kN')
                        p1.axes_dnm.plot(
                            momento_max_x, momento_max_y,  marker='x',
                            markersize=10, color='red',
                            label=f'Mmax= {round(momento_max_x, 2)} kN*m, '
                            f'N={round(momento_max_y,2)} kN')
                        p1.axes_dnm.plot(
                            momento_max_x * (-1), momento_max_y, marker='x',
                            markersize=10, color='red')

                    else:
                        lista_x = p1.lista_pontos_mx_x_2014
                        lista_y = p1.lista_pontos_mx_y_2014
                        lista_x_ambas = p1.lista_pontos_mx_x_2023
                        lista_y_ambas = p1.lista_pontos_mx_y_2023
                        p1.axes_dnm.plot(
                            lista_x, lista_y, color='blue',
                            label='ABNT NBR 6118:2014', linestyle='dashed')
                        ponto_tracao_maximo = max(lista_y)
                        ponto_compressao_maximo = min(lista_y)
                        momento_max_x = max(lista_x)
                        index_momento_max = lista_x.index(momento_max_x)
                        momento_max_y = lista_y[index_momento_max]
                        p1.pontos_tracao_max = p1.axes_dnm.plot(
                            0, ponto_tracao_maximo, marker='p', markersize=10,
                            color='blue', label='Nmax (tração)= '
                            f'{round(ponto_tracao_maximo, 2)} kN')
                        p1.axes_dnm.plot(
                            0, ponto_compressao_maximo, marker='o',
                            markersize=10, color='blue',
                            label=f'Nmin (compressão)= '
                            f'{round(ponto_compressao_maximo, 2)} kN')
                        p1.axes_dnm.plot(
                            momento_max_x, momento_max_y, marker='x',
                            markersize=10, color='blue',
                            label=f'Mmax= {round(momento_max_x, 2)} kN*m, '
                            f'N={round(momento_max_y,2)} kN')
                        p1.axes_dnm.plot(
                            momento_max_x * (-1), momento_max_y, marker='x',
                            markersize=10, color='blue')

                        p1.axes_dnm.plot(
                            lista_x_ambas, lista_y_ambas, color='red',
                            label='ABNT NBR 6118:2023')
                        ponto_tracao_maximo_ambas = max(lista_y_ambas)
                        ponto_compressao_maximo_ambas = min(lista_y_ambas)
                        momento_max_x_ambas = max(lista_x_ambas)
                        index_momento_max_ambas = lista_x_ambas.index(
                            momento_max_x_ambas)
                        momento_max_y_ambas = lista_y_ambas[
                            index_momento_max_ambas]
                        p1.pontos_tracao_max = p1.axes_dnm.plot(
                            0, ponto_tracao_maximo_ambas, marker='p',
                            markersize=10, color='red',
                            label='Nmax (tração)= '
                            f'{round(ponto_tracao_maximo_ambas, 2)} kN')
                        p1.axes_dnm.plot(
                            0, ponto_compressao_maximo_ambas, marker='o',
                            markersize=10, color='red',
                            label='Nmin (compressão)= '
                            f'{round(ponto_compressao_maximo_ambas, 2)} kN')
                        p1.axes_dnm.plot(
                            momento_max_x_ambas, momento_max_y_ambas,
                            marker='x', markersize=10, color='red',
                            label=f'Mmax= {round(momento_max_x_ambas, 2)} '
                            f'kN*m, N={round(momento_max_y_ambas,2)} kN')
                        p1.axes_dnm.plot(
                            momento_max_x_ambas * (-1), momento_max_y_ambas,
                            marker='x', markersize=10, color='red')

                else:
                    p1.axes_dnm.set_title(
                        'Diagrama de Interação N-My (FCN)', fontsize=26)
                    if self.norma_selecionada == '2014':
                        lista_x = p1.lista_pontos_my_x_2014
                        lista_y = p1.lista_pontos_my_y_2014
                        p1.axes_dnm.plot(
                            lista_x, lista_y, color='blue',
                            label='ABNT NBR 6118:2014')
                        ponto_compressao_maximo = min(lista_y)
                        ponto_tracao_maximo = max(lista_y)
                        momento_max_x = max(lista_x)
                        momento_min_x = momento_max_x * (-1)
                        index_momento_max = lista_x.index(momento_max_x)
                        momento_max_y = lista_y[index_momento_max]
                        p1.pontos_tracao_max = p1.axes_dnm.plot(
                            0, ponto_tracao_maximo, marker='p', markersize=10,
                            color='blue', label='Nmax (tração)= '
                            f'{round(ponto_tracao_maximo, 2)} kN')
                        p1.axes_dnm.plot(
                            0, ponto_compressao_maximo, marker='o',
                            markersize=10, color='blue',
                            label='Nmin (compressão)= '
                            f'{round(ponto_compressao_maximo, 2)} kN')
                        p1.axes_dnm.plot(
                            momento_max_x, momento_max_y, marker='x',
                            markersize=10, color='blue',
                            label=f'Mmax= {round(momento_max_x, 2)} kN*m, '
                            f'N={round(momento_max_y,2)} kN')
                        p1.axes_dnm.plot(
                            momento_min_x, momento_max_y, marker='x',
                            markersize=10, color='blue')

                    elif self.norma_selecionada == '2023':
                        lista_x = p1.lista_pontos_my_x_2023
                        lista_y = p1.lista_pontos_my_y_2023
                        p1.axes_dnm.plot(
                            lista_x, lista_y, color='red',
                            label='ABNT NBR 6118:2023')
                        ponto_tracao_maximo = max(lista_y)
                        ponto_compressao_maximo = min(lista_y)
                        momento_max_x = max(lista_x)
                        index_momento_max = lista_x.index(momento_max_x)
                        momento_max_y = lista_y[index_momento_max]
                        p1.pontos_tracao_max = p1.axes_dnm.plot(
                            0, ponto_tracao_maximo, marker='p', markersize=10,
                            color='red', label='Nmax (tração)= '
                            f'{round(ponto_tracao_maximo, 2)} kN')
                        p1.axes_dnm.plot(
                            0, ponto_compressao_maximo, marker='o',
                            markersize=10, color='red',
                            label='Nmin (compressão)= '
                            f'{round(ponto_compressao_maximo, 2)} kN')
                        p1.axes_dnm.plot(
                            momento_max_x, momento_max_y,  marker='x',
                            markersize=10, color='red',
                            label=f'Mmax= {round(momento_max_x, 2)} kN*m, '
                            f'N={round(momento_max_y,2)} kN')
                        p1.axes_dnm.plot(
                            momento_max_x * (-1), momento_max_y, marker='x',
                            markersize=10, color='red')

                    else:
                        lista_x = p1.lista_pontos_my_x_2014
                        lista_y = p1.lista_pontos_my_y_2014
                        lista_x_ambas = p1.lista_pontos_my_x_2023
                        lista_y_ambas = p1.lista_pontos_my_y_2023
                        p1.axes_dnm.plot(
                            lista_x, lista_y, color='blue',
                            label='ABNT NBR 6118:2014', linestyle='dashed')
                        ponto_tracao_maximo = max(lista_y)
                        ponto_compressao_maximo = min(lista_y)
                        momento_max_x = max(lista_x)
                        index_momento_max = lista_x.index(momento_max_x)
                        momento_max_y = lista_y[index_momento_max]
                        p1.pontos_tracao_max = p1.axes_dnm.plot(
                            0, ponto_tracao_maximo, marker='p',
                            markersize=10, color='blue',
                            label=f'Nmax (tração)= '
                            f'{round(ponto_tracao_maximo, 2)} kN')
                        p1.axes_dnm.plot(
                            0, ponto_compressao_maximo, marker='o',
                            markersize=10, color='blue',
                            label=f'Nmin (compressão)= '
                            f'{round(ponto_compressao_maximo, 2)} kN')
                        p1.axes_dnm.plot(
                            momento_max_x, momento_max_y, marker='x',
                            markersize=10, color='blue',
                            label=f'Mmax= {round(momento_max_x, 2)} kN*m, '
                            f'N={round(momento_max_y,2)} kN')
                        p1.axes_dnm.plot(
                            momento_max_x * (-1), momento_max_y, marker='x',
                            markersize=10, color='blue')

                        p1.axes_dnm.plot(
                            lista_x_ambas, lista_y_ambas, color='red',
                            label='ABNT NBR 6118:2023')
                        ponto_tracao_maximo_ambas = max(lista_y_ambas)
                        ponto_compressao_maximo_ambas = min(lista_y_ambas)
                        momento_max_x_ambas = max(lista_x_ambas)
                        index_momento_max_ambas = lista_x_ambas.index(
                            momento_max_x_ambas)
                        momento_max_y_ambas = lista_y_ambas[
                            index_momento_max_ambas]
                        p1.pontos_tracao_max = p1.axes_dnm.plot(
                            0, ponto_tracao_maximo_ambas, marker='p',
                            markersize=10, color='red',
                            label='Nmax (tração)= '
                            f'{round(ponto_tracao_maximo_ambas, 2)} kN')
                        p1.axes_dnm.plot(
                            0, ponto_compressao_maximo_ambas, marker='o',
                            markersize=10, color='red',
                            label=f'Nmin (compressão)= '
                            f'{round(ponto_compressao_maximo_ambas, 2)} kN')
                        p1.axes_dnm.plot(
                            momento_max_x_ambas, momento_max_y_ambas,
                            marker='x', markersize=10, color='red',
                            label=f'Mmax= {round(momento_max_x_ambas, 2)} '
                            f'kN*m, N={round(momento_max_y_ambas,2)} kN')
                        p1.axes_dnm.plot(
                            momento_max_x_ambas * (-1), momento_max_y_ambas,
                            marker='x', markersize=10, color='red')

                p1.axes_dnm.set_xlim(
                    min(lista_x) - (0.25 * max(lista_x)),
                    max(lista_x) + (0.25 * max(lista_x)))
                p1.axes_dnm.set_ylim(
                    min(lista_y) - (0.25 * max(lista_y)),
                    max(lista_y) + (0.25 * max(lista_y)))
                p1.axes_dnm.legend(loc='lower left', facecolor='none')

                self.desenho_diagrama_n_m.draw()

        def button_tela_diag_td():
            tela_diagramas_td = Tk()
            tela_diagramas_td.title(
                'Diagrmas Tensão X Deformação - Desenvolvido por João Paulo '
                'da Silva Sabedotti')
            tela_diagramas_td.geometry('1000x680+180+10')
            TelaDiagramasTensaoDeformacao(tela_diagramas_td)
            root.mainloop()

        # Containers
        self.tela = master
        self.container1 = Frame(self.tela, height=352.5, width=683,
                                highlightbackground='black',
                                highlightthickness=2)
        self.container1.place(x=0, y=0)

        self.container1_1 = Frame(self.container1, height=310, width=335,
                                  highlightbackground='black',
                                  highlightthickness=1)
        self.container1_1.place(x=10, y=30)

        self.container1_3 = Frame(self.container1, height=310, width=310,
                                  highlightbackground='black',
                                  highlightthickness=1)
        self.container1_3.place(x=355, y=30)

        self.container2 = Frame(self.tela, height=705, width=683,
                                highlightbackground='black',
                                highlightthickness=2)
        self.container2.place(x=683, y=0)

        self.container2_1 = Frame(self.container2, height=705, width=663,
                                  highlightbackground='black',
                                  highlightthickness=2)
        self.container2_1.place(x=683, y=0)

        self.container2_2 = Frame(self.container2, height=500, width=663,
                                  highlightbackground='black',
                                  highlightthickness=2)
        self.container2_2.place(x=10, y=110)

        self.container3 = Frame(self.tela, height=352.5, width=683,
                                highlightbackground='black',
                                highlightthickness=2)
        self.container3.place(x=0, y=352.5)

        self.container3_1 = Frame(self.container3, height=310, width=335,
                                  highlightbackground='black',
                                  highlightthickness=1)
        self.container3_1.place(x=10, y=30)

        self.container3_2 = Frame(self.container3, height=310, width=310,
                                  highlightbackground='black',
                                  highlightthickness=1)
        self.container3_2.place(x=355, y=30)

        # Dados para Seção Transversal
        self.title_st = Label(
            self.container1, text='Dados da Seção Transversal',
            font=('arial', 16, 'bold'))
        self.title_st.place(x=200, y=0)

        self.lbl_dim_x = Label(self.container1_1, text='Dimensão x:')
        self.lbl_dim_x['font'] = (fonte, 12)
        self.lbl_dim_x.place(x=10, y=10)

        self.entry_dim_x = Entry(self.container1_1)
        self.entry_dim_x['font'] = (fonte, 12)
        self.entry_dim_x.place(x=110, y=13, width=40, height=20)

        self.cm_dim_x = Label(self.container1_1, text='cm')
        self.cm_dim_x['font'] = (fonte, 12)
        self.cm_dim_x.place(x=155, y=10)

        self.lbl_dim_y = Label(self.container1_1, text='Dimensão y:')
        self.lbl_dim_y['font'] = (fonte, 12)
        self.lbl_dim_y.place(x=10, y=40)

        self.entry_dim_y = Entry(self.container1_1)
        self.entry_dim_y['font'] = (fonte, 12)
        self.entry_dim_y.place(x=110, y=43, width=40, height=20)

        self.cm_dim_y = Label(self.container1_1, text='cm')
        self.cm_dim_y['font'] = (fonte, 12)
        self.cm_dim_y.place(x=155, y=40)

        self.lbl_nx = Label(self.container1_1, text='Número de Barras em X:')
        self.lbl_nx['font'] = (fonte, 12)
        self.lbl_nx.place(x=10, y=70)

        self.entry_nx = Entry(self.container1_1)
        self.entry_nx['font'] = (fonte, 12)
        self.entry_nx.place(x=195, y=73, width=40, height=20)

        self.barras_nx = Label(self.container1_1, text='barras')
        self.barras_nx['font'] = (fonte, 12)
        self.barras_nx.place(x=240, y=70)

        self.lbl_ny = Label(self.container1_1, text='Número de Barras em Y:')
        self.lbl_ny['font'] = (fonte, 12)
        self.lbl_ny.place(x=10, y=100)

        self.entry_ny = Entry(self.container1_1)
        self.entry_ny['font'] = (fonte, 12)
        self.entry_ny.place(x=195, y=103, width=40, height=20)

        self.barras_ny = Label(self.container1_1, text='barras')
        self.barras_ny['font'] = (fonte, 12)
        self.barras_ny.place(x=240, y=100)

        self.lbl_dlinha = Label(self.container1_1, text="Espaçamento d':")
        self.lbl_dlinha['font'] = (fonte, 12)
        self.lbl_dlinha.place(x=10, y=130)

        self.entry_dlinha = Entry(self.container1_1)
        self.entry_dlinha['font'] = (fonte, 12)
        self.entry_dlinha.place(x=140, y=133, width=40, height=20)

        self.cm_dlinha = Label(self.container1_1, text='cm')
        self.cm_dlinha['font'] = (fonte, 12)
        self.cm_dlinha.place(x=185, y=130)

        self.lbl_bitola = Label(self.container1_1, text='Bitola de aço:')
        self.lbl_bitola['font'] = (fonte, 12)
        self.lbl_bitola.place(x=10, y=160)

        self.listbox_bitola = Combobox(self.container1_1, values=lista_bitolas)
        self.listbox_bitola['font'] = (fonte, 12)
        self.listbox_bitola.place(x=120, y=163, width=60, height=20)

        self.mm_bitola = Label(self.container1_1, text='mm')
        self.mm_bitola['font'] = (fonte, 12)
        self.mm_bitola.place(x=185, y=160)

        img = PhotoImage(file='programa_tcc\\imagem_st_inicial.png')
        self.lbl = Label(self.container1_3, image=img)
        self.lbl.image = img  # type: ignore
        self.lbl.place(x=0, y=0)

        self.lbl_erro_variaveis = Label(
            self.container1_1, text='', foreground='red', font=(fonte, 10))
        self.lbl_erro_variaveis.place(x=80, y=195)

        self.button_confirmar = Button(
            self.container1_1, text='Confirmar Seção Transversal',
            background='light blue')
        self.button_confirmar['font'] = (fonte, 12)
        self.button_confirmar['command'] = button_confirm_st
        self.button_confirmar.place(x=60, y=225)

        self.button_erros = Button(
            self.container1_1, text='Considerações Normativas',
            background='light blue')
        self.button_erros['font'] = (fonte, 12)
        self.button_erros['command'] = tela_consideracoes_norma
        self.button_erros.place(x=67, y=265)

        # Dados dos materiais
        self.title_st = Label(
            self.container3, text='Características dos Materiais',
            font=('arial', 16, 'bold'))
        self.title_st.place(x=30, y=0)

        self.lbl_dados_concreto = Label(
            self.container3_1, text='Dados para Concreto')
        self.lbl_dados_concreto['font'] = (fonte, 12, 'bold')
        self.lbl_dados_concreto.place(x=80, y=5)

        self.lbl_fck_1 = Label(
            self.container3_1, text='Resistência Característica do')
        self.lbl_fck_1['font'] = (fonte, 12)
        self.lbl_fck_1.place(x=10, y=30)

        self.lbl_fck_2 = Label(
            self.container3_1, text='Concreto à Compressão - fck:')
        self.lbl_fck_2['font'] = (fonte, 12)
        self.lbl_fck_2.place(x=10, y=50)

        self.combobox_fck = Combobox(
            self.container3_1, values=classes_concreto_str)
        self.combobox_fck['font'] = (fonte, 12)
        self.combobox_fck.place(x=230, y=42, width=40, height=20)

        self.mpa_fck = Label(self.container3_1, text='MPa')
        self.mpa_fck['font'] = (fonte, 12)
        self.mpa_fck.place(x=275, y=41)

        self.lbl_gama_c = Label(self.container3_1, text='Coeficiente γc:')
        self.lbl_gama_c['font'] = (fonte, 12)
        self.lbl_gama_c.place(x=10, y=80)

        self.entry_gama_c = Entry(self.container3_1)
        self.entry_gama_c['font'] = (fonte, 12)
        self.entry_gama_c.insert(0, '1.4')
        self.entry_gama_c.place(x=123, y=82, width=40, height=20)

        self.lbl_dados_aco = Label(
            self.container3_1, text='Dados para Armaduras de Aço')
        self.lbl_dados_aco['font'] = (fonte, 12, 'bold')
        self.lbl_dados_aco.place(x=50, y=110)

        self.lbl_fyk_1 = Label(
            self.container3_1, text='Resistência Característica ao')
        self.lbl_fyk_1['font'] = (fonte, 12)
        self.lbl_fyk_1.place(x=10, y=140)

        self.lbl_fyk_2 = Label(
            self.container3_1, text='Escoamento do Aço - fyk:')
        self.lbl_fyk_2['font'] = (fonte, 12)
        self.lbl_fyk_2.place(x=10, y=160)

        self.entry_fyk = Entry(self.container3_1)
        self.entry_fyk['font'] = (fonte, 12)
        self.entry_fyk.place(x=230, y=152, width=40, height=20)

        self.mpa_fyk = Label(self.container3_1, text='MPa')
        self.mpa_fyk['font'] = (fonte, 12)
        self.mpa_fyk.place(x=275, y=152)

        self.lbl_mod_elast = Label(
            self.container3_1, text='Módulo Elasticidade - Es:')
        self.lbl_mod_elast['font'] = (fonte, 12)
        self.lbl_mod_elast.place(x=10, y=190)

        self.entry_mod_elast = Entry(self.container3_1)
        self.entry_mod_elast['font'] = (fonte, 12)
        self.entry_mod_elast.insert(0, '210000')
        self.entry_mod_elast.place(x=200, y=192, width=70, height=20)

        self.mpa_mod_elast = Label(self.container3_1, text='MPa')
        self.mpa_mod_elast['font'] = (fonte, 12)
        self.mpa_mod_elast.place(x=275, y=190)

        self.lbl_gama_s = Label(self.container3_1, text='Coeficiente γs:')
        self.lbl_gama_s['font'] = (fonte, 12)
        self.lbl_gama_s.place(x=10, y=220)

        self.entry_gama_s = Entry(self.container3_1)
        self.entry_gama_s['font'] = (fonte, 12)
        self.entry_gama_s.insert(0, '1.15')
        self.entry_gama_s.place(x=123, y=222, width=40, height=20)

        self.lbl_erro_materiais = Label(
            self.container3_1, text='', foreground='red', font=(fonte, 10))
        self.lbl_erro_materiais.place(x=75, y=245)

        self.button_confirmar_materiais = Button(
            self.container3_1, text='Confirmar Características dos Materiais',
            background='light blue')
        self.button_confirmar_materiais['font'] = (fonte, 12)
        self.button_confirmar_materiais['command'] = button_confirm_caract_mat
        self.button_confirmar_materiais.place(x=20, y=270)

        self.title_st = Label(
            self.container3, text='Dados Adicionais',
            font=('arial', 16, 'bold'))
        self.title_st.place(x=425, y=0)

        self.lbl_area_aco = Label(
            self.container3_2, text=f'Área de Aço: {p1.area_aco} cm²')
        self.lbl_area_aco['font'] = (fonte, 11)
        self.lbl_area_aco.place(x=10, y=10)

        self.lbl_area_concreto = Label(
            self.container3_2,
            text=f'Área de Concreto: {p1.area_concreto} cm²')
        self.lbl_area_concreto['font'] = (fonte, 11)
        self.lbl_area_concreto.place(x=10, y=40)

        self.lbl_taxa_armadura = Label(
            self.container3_2, text=f'Taxa de Armadura: {p1.taxa_armadura}%')
        self.lbl_taxa_armadura['font'] = (fonte, 11)
        self.lbl_taxa_armadura.place(x=10, y=70)

        self.lbl_fcd_1 = Label(
            self.container3_2, text='Resistência de Calculo do')
        self.lbl_fcd_1['font'] = (fonte, 11)
        self.lbl_fcd_1.place(x=10, y=100)

        self.lbl_fcd_2 = Label(
            self.container3_2, text='Concreto à Compressão - fcd:')
        self.lbl_fcd_2['font'] = (fonte, 11)
        self.lbl_fcd_2.place(x=10, y=120)

        self.lbl_fcd_3 = Label(self.container3_2, text=f'{p1.fcd}MPa')
        self.lbl_fcd_3['font'] = (fonte, 11)
        self.lbl_fcd_3.place(x=220, y=110)

        self.lbl_fyd_1 = Label(
            self.container3_2, text='Resistência de Calculo do')
        self.lbl_fyd_1['font'] = (fonte, 11)
        self.lbl_fyd_1.place(x=10, y=150)

        self.lbl_fyd_2 = Label(
            self.container3_2, text='Aço à Compressão - fyd:')
        self.lbl_fyd_2['font'] = (fonte, 11)
        self.lbl_fyd_2.place(x=10, y=170)

        self.lbl_fyd_3 = Label(self.container3_2, text=f'{p1.fyd}MPa')
        self.lbl_fyd_3['font'] = (fonte, 11)
        self.lbl_fyd_3.place(x=197, y=162)

        self.button_tela_diag_td = Button(
            self.container3_2, text='Diagramas de Tensão X Deformação',
            background='light blue')
        self.button_tela_diag_td['font'] = (fonte, 12)
        self.button_tela_diag_td['command'] = button_tela_diag_td
        self.button_tela_diag_td.place(x=20, y=200)

        self.title_diagramas_interação = Label(
            self.container2,
            text='Diagramas de Interação - Flexo-Compressão Normal',
            font=('arial', 16, 'bold'))
        self.title_diagramas_interação.place(x=80, y=0)

        self.lbl_norma = Label(self.container2, text='Norma ABNT NBR 6118:')
        self.lbl_norma['font'] = (fonte, 12)
        self.lbl_norma.place(x=10, y=40)

        self.combobox_norma = Combobox(self.container2, values=anos_norma)
        self.combobox_norma['font'] = (fonte, 12)
        self.combobox_norma.place(x=190, y=42, width=80, height=20)

        self.lbl_sentido_diagrama = Label(
            self.container2, text='Sentido do Diagrama de Interação:')
        self.lbl_sentido_diagrama['font'] = (fonte, 12)
        self.lbl_sentido_diagrama.place(x=10, y=70)

        self.combobox_sentido = Combobox(
            self.container2, values=sentido_diagrama_n_m)
        self.combobox_sentido['font'] = (fonte, 12)
        self.combobox_sentido.place(x=260, y=72, width=70, height=20)

        self.button_confirmar_norma = Button(
            self.container2, text='Gerar Diagrama de Interação N-M',
            background='light blue')
        self.button_confirmar_norma['font'] = (fonte, 12)
        self.button_confirmar_norma['command'] = gerar_diagrama_n_m
        self.button_confirmar_norma.place(x=385, y=35)

        self.lbl_erro_geracao_diagrama = Label(
            self.container2, text='', font=(fonte, 10))
        self.lbl_erro_geracao_diagrama.place(x=365, y=75)

        p1.axes_dnm.set_ylabel('Força Normal (kN)')
        p1.axes_dnm.set_xlabel('Momento (kN*m)')
        p1.axes_dnm.grid(True, 'both', 'both')
        p1.axes_dnm.set_title('Diagramas de Interação N-M (FCN)', fontsize=26)
        p1.axes_dnm.set_xlim(-5000, 5000)
        p1.axes_dnm.set_ylim(-5000, 5000)

        self.desenho_diagrama_n_m = FigureCanvasTkAgg(
            p1.figura_diagrama, self.container2_2)
        self.desenho_diagrama_n_m.draw()
        toolbar = NavigationToolbar2Tk(
            self.desenho_diagrama_n_m, self.container2_2)
        self.desenho_diagrama_n_m.get_tk_widget().pack()
        toolbar.update()


root = Tk()
root.title('ResisPilar - Desenvolvido por João Paulo da Silva Sabedotti')
root.geometry('1366x705')
root.state(newstate='zoomed')
app = Aplication(root)
root.mainloop()
