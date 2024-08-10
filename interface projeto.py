from tkinter import *

janela = Tk()
class aplicacao():
    def __init__(self):
        self.janela = janela
        self .tela()
        self.frames_da_dela()
        self.botoesFrame_1()
        janela.mainloop()

    def tela(self): #temos todas as configurações da tela
        self.janela.title("FLUXO DE CAIXA") #titulo da janela
        self.janela.configure(background= '#1e3743') #cor de fundo
        self.janela.geometry ("700x300") #porporção da tela
        self.janela.resizable(True, True) #flexibilidade da tela
        self.janela.maxsize(width=900,height=700)
        self.janela.minsize(width=400,height=300)

    def frames_da_dela(self):
        self.frame_1 = Frame(self.janela, bd=4 , bg = '#436778', highlightbackground ='#2c4c5c', highlightthickness=3)
        self.frame_1.place(relx=0.02,rely=0.04,relwidth = 0.96,relheight=0.40)

        self.frame_2 = Frame(self.janela, bd=4, bg='#436778', highlightbackground='#2c4c5c', highlightthickness=3)
        self.frame_2.place(relx=0.02, rely=0.50, relwidth=0.96, relheight=0.40)

    def botoesFrame_1(self):
        #botão adicionar
        self.bot_adicionar = Button(self.frame_1, text="ADICIONAR")
        self.bot_adicionar.place(relx= 0.1, rely=0.80,relwidth=0.1 ,relheight=0.15)

        # botão buscar
        self.bot_buscar = Button(self.frame_1, text="BUSCAR")
        self.bot_buscar.place(relx=0.3, rely=0.80, relwidth=0.1, relheight=0.15)

        # botão apagar
        self.bot_apagar = Button(self.frame_1, text="APAGAR")
        self.bot_apagar.place(relx=0.5, rely=0.80, relwidth=0.1, relheight=0.15)

        # botão editar
        self.bot_editar = Button(self.frame_1, text="EDITAR")
        self.bot_editar.place(relx=0.7, rely=0.80, relwidth=0.1, relheight=0.15)


    #criando as label e entradas de dados:

        # label busca
        self.lb_buscar = Label(self.frame_1, text="procurar",bg='#436778')
        self.lb_buscar.place(relx=0.025, rely=0.01)
        #entrada busca
        self.buscar_entry= Entry(self.frame_1)
        self.buscar_entry.place(relx=0.01,rely=0.15,relwidth=0.1, relheight=0.15)

# label nome
        self.lb_nome = Label(self.frame_1, text="Nome",bg='#436778')
        self.lb_nome.place(relx=0.15, rely=0.01)
        #entrada nome
        self.nome_entry= Entry(self.frame_1)
        self.nome_entry.place(relx=0.15,rely=0.15,relwidth=0.25, relheight=0.15)

        # label dia
        self.lb_dia = Label(self.frame_1, text="dia", bg='#436778')
        self.lb_dia.place(relx=0.45, rely=0.01)
        # entrada dia
        self.dia_entry = Entry(self.frame_1)
        self.dia_entry.place(relx=0.45, rely=0.15, relwidth=0.05, relheight=0.15)

        # label mês
        self.lb_mes = Label(self.frame_1, text="mês", bg='#436778')
        self.lb_mes.place(relx=0.55, rely=0.01)
        # entrada mês
        self.mes_entry = Entry(self.frame_1)
        self.mes_entry.place(relx=0.55, rely=0.15, relwidth=0.05, relheight=0.15)
 # label ano
        self.lb_ano = Label(self.frame_1, text="ano", bg='#436778')
        self.lb_ano.place(relx=0.65, rely=0.01)
        # entrada ano
        self.ano_entry = Entry(self.frame_1)
        self.ano_entry.place(relx=0.65, rely=0.15, relwidth=0.10, relheight=0.15)


aplicacao()
