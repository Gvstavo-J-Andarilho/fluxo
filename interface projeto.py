from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime
import sqlite3


class Funcoes():
    def apagar_tela(self):
        self.buscar_entry.delete(0, END)
        self.valor_entry.delete(0, END)
        self.nome_entry.delete(0, END)

    def conecta_bd(self):
        self.conec = sqlite3.connect("clientes.bd")
        self.cursor = self.conec.cursor()

    def desconectar_bd(self):
        self.conec.close()
        #self.select_lista()
        #self.apagar_tela()

    def montaTabelas(self):
        self.conecta_bd();
        print("Conectando banco de dados")
        ###   Criar tabela
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS lancamento (
            data TEXT NOT NULL,
            valor REAL NOT NULL,
            tipo TEXT NOT NULL,
            nome TEXT,
            saldo REAL


        );
    """)
        self.conec.commit();
        print("Banco de dados criado")
        self.desconectar_bd;
        print("Banco de dados desconectado")

    def add_lancamento(self):
        if not self.data_numerica:
            # Se a data não foi selecionada, exiba uma mensagem de erro
            print("Erro: Data não selecionada.")
            return

        self.conecta_bd()

        # Recupera o último saldo da tabela, ordenado por data
        self.cursor.execute("SELECT saldo FROM lancamento ORDER BY data DESC LIMIT 1")
        resultado = self.cursor.fetchone()

        # Se houver registros, pega o saldo atual; caso contrário, começa com 0
        saldo_atual = resultado[0] if resultado else 0

        self.valor = float(self.valor_entry.get().replace(",", "."))
        self.valor = round(self.valor,2)
        print(round(self.valor,2))
        self.nome = self.nome_entry.get()

        if self.tipo_lancamento == "entrada":
            saldo_atual += self.valor
        elif self.tipo_lancamento == "saida":
            saldo_atual -= self.valor

        # Insere o novo lançamento com o saldo atualizado
        self.cursor.execute(""" 
            INSERT INTO lancamento (data, valor, tipo, nome, saldo) 
            VALUES(?,?,?,?,?)""", (self.data_numerica, self.valor, self.tipo_lancamento, self.nome, saldo_atual))

        self.conec.commit()
        self.desconectar_bd()
        self.select_lista()  # Atualiza a lista com o novo saldo

    def select_lista(self):
        self.lanca_frame2.delete(
            *self.lanca_frame2.get_children())
        self.conecta_bd()
        lista = self.cursor.execute(""" SELECT data, valor, tipo, nome, saldo FROM lancamento
          ORDER BY nome ASC; """)
        for i in lista:
            self.lanca_frame2.insert("", END, values=i)
        self.desconectar_bd()


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
        self.montaTabelas()
        self.data_numerica = None
        self.calendario_app = None
        self.tipo_lancamento = None
        self.select_lista()

        self.janela.mainloop()

    def abrir_calendario(self):
        # Inicializa a aplicação do calendário dentro da janela principal
        self.calendario_app = AplicacaoCalendario(self.janela, self)

    def definir_tipo_entrada(self):
        self.tipo_lancamento = "entrada"
        self.bot_entrada.config(state=DISABLED)
        self.bot_saida.config(state=DISABLED)
        self.bot_adicionar.config(state=NORMAL)

    def definir_tipo_saida(self):
        self.tipo_lancamento = "saida"
        self.bot_entrada.config(state=DISABLED)
        self.bot_saida.config(state=DISABLED)
        self.bot_adicionar.config(state=NORMAL)

    def frames_da_tela(self):  # frame = retangulos da tela
        # tela de cima
        self.frame_1 = Frame(self.janela, bd=4, bg='#436778', highlightbackground='#2c4c5c', highlightthickness=3)
        self.frame_1.place(relx=0.02, rely=0.04, relwidth=0.96, relheight=0.40)
        # tela de baixo
        self.frame_2 = Frame(self.janela, bd=4, bg='#436778', highlightbackground='#2c4c5c', highlightthickness=3)
        self.frame_2.place(relx=0.02, rely=0.50, relwidth=0.96, relheight=0.40)

    def botoesFrame_1(self):  # botão adicionar
        self.bot_adicionar = Button(self.frame_1, text="ADICIONAR", bd=2, bg='#abcad9', fg="black",
                                    font=("verdana", 8, "bold"), command=self.add_lancamento)
        self.bot_adicionar.place(relx=0.1, rely=0.80, relwidth=0.12, relheight=0.12)

        # botão buscar
        self.bot_buscar = Button(self.frame_1, text="BUSCAR", bd=2, bg='#abcad9', fg="black",
                                 font=("verdana", 8, "bold"))
        self.bot_buscar.place(relx=0.3, rely=0.80, relwidth=0.1, relheight=0.12)

        # botão apagar
        self.bot_apagar = Button(self.frame_1, text="APAGAR", bd=2, bg='#abcad9', fg="black",
                                 font=("verdana", 8, "bold"), command=self.apagar_tela)
        self.bot_apagar.place(relx=0.5, rely=0.80, relwidth=0.1, relheight=0.12)

        # botão editar
        self.bot_editar = Button(self.frame_1, text="EDITAR", bd=2, bg='#abcad9', fg="black",
                                 font=("verdana", 8, "bold"))
        self.bot_editar.place(relx=0.7, rely=0.80, relwidth=0.1, relheight=0.12)

        # botão entrada
        self.bot_entrada = Button(self.frame_1, text="INSERIR ENTRADA", bd=2, bg='#48ab4d', fg="black",
                                  font=("verdana", 8, "bold"), command=self.definir_tipo_entrada)
        self.bot_entrada.place(relx=0.5, rely=0.65, relwidth=0.20, relheight=0.10)

        # botão saida
        self.bot_saida = Button(self.frame_1, text="INSERIR SAIDA", bd=2, bg='#ab4848', fg="black",
                                font=("verdana", 8, "bold"), command=self.definir_tipo_saida)
        self.bot_saida.place(relx=0.25, rely=0.65, relwidth=0.20, relheight=0.10)

        # botão data
        self.bot_data = Button(self.frame_1, text="Data", bd=2, bg='#abcad9', fg="black", font=("verdana", 8, "bold"),
                               command=self.abrir_calendario)
        self.bot_data.place(relx=0.75, rely=0.30, relwidth=0.1, relheight=0.12)

        # Label = espaço de escrever/entrada

        # Label buscar
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
        self.lanca_frame2 = ttk.Treeview(self.frame_2, height=3, column=("col1", "col2", "col3", "col4", "col5"))
        self.lanca_frame2.heading("#0", text="")
        self.lanca_frame2.heading("#1", text="Data")
        self.lanca_frame2.heading("#2", text="Valor")
        self.lanca_frame2.heading("#3", text="Tipo")
        self.lanca_frame2.heading("#4", text="Nome")
        self.lanca_frame2.heading("#5", text="Saldo")

        self.lanca_frame2.column("#0", width=0, stretch=NO)  # Coluna escondida
        self.lanca_frame2.column("#1", width=150)
        self.lanca_frame2.column("#2", width=100)
        self.lanca_frame2.column("#3", width=50)
        self.lanca_frame2.column("#4", width=150)
        self.lanca_frame2.column("#5", width=100)

        self.lanca_frame2.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)

        self.scrollLista = Scrollbar(self.frame_2, orient="vertical")
        self.lanca_frame2.configure(yscroll=self.scrollLista.set)
        self.scrollLista.place(relx=0.96, rely=0.1, relwidth=0.03, relheight=.85)


# Classe do calendário para chamar na principal
class AplicacaoCalendario:
    def __init__(self, root, app_ref):
        self.root = root
        self.app_ref = app_ref  # Referência para a classe principal
        self.mostrar_calendario()

    def mostrar_calendario(self):
        hoje = datetime.now().date()
        mes_atual = hoje.month
        ano_atual = hoje.year
        self.calendario = Calendar(self.root, selectmode='day', locale='pt_br', year=ano_atual, month=mes_atual,
                                   day=hoje.day)
        self.calendario.place(relx=0.75, rely=0.30, anchor="center")
        self.calendario.bind("<<CalendarSelected>>", self.coletar_data)

    def coletar_data(self, event):
        data_selecionada = self.calendario.get_date()
        data_numerica = datetime.strptime(data_selecionada, "%d/%m/%Y").strftime("%d/%m/%Y")
        print(data_numerica)
        self.app_ref.data_numerica = data_numerica  # Armazena a data na instância principal
        self.calendario.destroy()


# Inicializa a aplicação principalF
aplicacao()
