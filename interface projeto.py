from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime


class Funcoes():
    def apagar_tela(self):
        self.buscar_entry.delete(0, END)
        self.valor_entry.delete(0, END)
        self.nome_entry.delete(0, END)
        self.data_entry.delete(0, END)


class aplicacao(Funcoes):
    def __init__(self):
        self.janela = Tk()
        self.janela.title("FLUXO DE CAIXA")
        self.janela.configure(background='#1e3743')
        self.janela.geometry("750x400")
        self.janela.resizable(True, True)
        self.janela.maxsize(width=900, height=700)
        self.janela.minsize(width=400, height=300)

        self.frames_da_tela()
        self.botoesFrame_1()
        self.lista_frame2()

        self.calendario_app = None  # Instância do calendário será armazenada aqui

        self.janela.mainloop()

    def frames_da_tela(self): #frame = retangulos da tela
        #tela de cima
        self.frame_1 = Frame(self.janela, bd=4, bg='#436778', highlightbackground='#2c4c5c', highlightthickness=3)
        self.frame_1.place(relx=0.02, rely=0.04, relwidth=0.96, relheight=0.40)
        #tela de baixo
        self.frame_2 = Frame(self.janela, bd=4, bg='#436778', highlightbackground='#2c4c5c', highlightthickness=3)
        self.frame_2.place(relx=0.02, rely=0.50, relwidth=0.96, relheight=0.40)

    def botoesFrame_1(self): #botão adicionar
        self.bot_adicionar = Button(self.frame_1, text="ADICIONAR", bd=2, bg='#abcad9', fg="black", font=("verdana", 8, "bold"))
        self.bot_adicionar.place(relx=0.1, rely=0.80, relwidth=0.12, relheight=0.12)

        # botão buscar
        self.bot_buscar = Button(self.frame_1, text="BUSCAR", bd=2, bg='#abcad9', fg="black", font=("verdana", 8, "bold"))
        self.bot_buscar.place(relx=0.3, rely=0.80, relwidth=0.1, relheight=0.12)

        # botão apagar
        self.bot_apagar = Button(self.frame_1, text="APAGAR", bd=2, bg='#abcad9', fg="black", font=("verdana", 8, "bold"), command=self.apagar_tela)
        self.bot_apagar.place(relx=0.5, rely=0.80, relwidth=0.1, relheight=0.12)

        # botão editar
        self.bot_editar = Button(self.frame_1, text="EDITAR", bd=2, bg='#abcad9', fg="black", font=("verdana", 8, "bold"))
        self.bot_editar.place(relx=0.7, rely=0.80, relwidth=0.1, relheight=0.12)

        # botão entrada
        self.bot_entrada = Button(self.frame_1, text="INSERIR ENTRADA", bd=2, bg='#48ab4d', fg="black", font=("verdana", 8, "bold"))
        self.bot_entrada.place(relx=0.5, rely=0.65, relwidth=0.20, relheight=0.10)

        # botão saida
        self.bot_saida = Button(self.frame_1, text="INSERIR SAIDA", bd=2, bg='#ab4848', fg="black", font=("verdana", 8, "bold"))
        self.bot_saida.place(relx=0.25, rely=0.65, relwidth=0.20, relheight=0.10)

        # botão data
        self.bot_data = Button(self.frame_1, text="Data", bd=2, bg='#abcad9', fg="black", font=("verdana", 8, "bold"), command=self.abrir_calendario)
        self.bot_data.place(relx=0.75, rely=0.30, relwidth=0.1, relheight=0.12)


        #Label = espaço de escrever/entrada

        #Label buscar
        self.lb_buscar = Label(self.frame_1, text="Buscar", bg='#436778', fg="black", font=("verdana", 9, "bold"))
        self.lb_buscar.place(relx=0.015, rely=0.01)
        # Texto da busca
        self.buscar_entry = Entry(self.frame_1)
        self.buscar_entry.place(relx=0.01, rely=0.15, relwidth=0.1, relheight=0.15)

        # Label nome
        self.lb_nome = Label(self.frame_1, text="Nome", bg='#436778', fg="black", font=("verdana", 11, "bold"))
        self.lb_nome.place(relx=0.15, rely=0.15)
        # Texto da nome
        self.nome_entry = Entry(self.frame_1)
        self.nome_entry.place(relx=0.15, rely=0.30, relwidth=0.25, relheight=0.10)

        # Label valor
        self.lb_valor = Label(self.frame_1, text="Valor", bg='#436778', fg="black", font=("verdana", 9, "bold"))
        self.lb_valor.place(relx=0.45, rely=0.42)
        # Texto da valor
        self.valor_entry = Entry(self.frame_1)
        self.valor_entry.place(relx=0.40, rely=0.53, relwidth=0.15, relheight=0.10)

    def lista_frame2(self):
        self.lanca_frame2 = ttk.Treeview(self.frame_2, height=3, column=("col1", "col2", "col3", "col4"))
        self.lanca_frame2.heading("#0", text="Data")
        self.lanca_frame2.heading("#1", text="Valor")
        self.lanca_frame2.heading("#2", text="Tipo")
        self.lanca_frame2.heading("#3", text="Nome")
        self.lanca_frame2.heading("#4", text="Saldo")

        self.lanca_frame2.column("#0", width=150)
        self.lanca_frame2.column("#1", width=100)
        self.lanca_frame2.column("#2", width=50)
        self.lanca_frame2.column("#3", width=150)
        self.lanca_frame2.column("#4", width=30)

        self.lanca_frame2.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)

        self.scrollLista = Scrollbar(self.frame_2, orient="vertical")
        self.lanca_frame2.configure(yscroll=self.scrollLista.set)
        self.scrollLista.place(relx=0.96, rely=0.1, relwidth=0.03, relheight=.85)

    def abrir_calendario(self):
        # Inicializa a aplicação do calendário dentro da janela principal
        self.calendario_app = AplicacaoCalendario(self.janela)

# Classe do calendário que será chamada na aplicação principal
class AplicacaoCalendario:
    def __init__(self, root):
        self.root = root
        self.mostrar_calendario()

    def mostrar_calendario(self):
        hoje = datetime.now().date()
        mes_atual = hoje.month
        ano_atual = hoje.year
        self.calendario = Calendar(self.root, selectmode='day', locale='pt_br', year=ano_atual, month=mes_atual, day=hoje.day)
        self.calendario.place(relx=0.5, rely=0.5, anchor="center")
        self.calendario.bind("<<CalendarSelected>>", self.coletar_data)

    def coletar_data(self, event):
        data_selecionada = self.calendario.get_date()
        data_numerica = datetime.strptime(data_selecionada, "%d/%m/%Y").strftime("%d/%m/%Y")
        print(data_numerica)
        self.calendario.destroy()

# Inicializa a aplicação principal
aplicacao()
