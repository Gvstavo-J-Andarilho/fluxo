import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import sqlite3
from datetime import datetime
from matplotlib.dates import DateFormatter


class DashboardFinanceiro(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Dashboard Financeiro")
        self.geometry("900x700")  # Ajuste para acomodar os gráficos e o botão

        # Definindo as cores principais
        self.bg_cor = "#436778"
        self.highlight_bg = "#2c4c5c"
        self.bg_janela = "#f4f4f9"
        self.text_cor = "#333333"
        self.title_cor = "#1e2a47"

        # Configurando a cor de fundo da janela principal
        self.config(bg=self.highlight_bg)

        # Adicionar seção para saldo
        self.saldo_label = tk.Label(self, text="Saldo Atual: R$ 0.00", font=("Arial", 18), fg=self.bg_janela, bg=self.highlight_bg)
        self.saldo_label.pack(pady=10)

        # Frame principal onde os gráficos serão dispostos
        self.frame_graficos = tk.Frame(self, bg=self.highlight_bg)
        self.frame_graficos.pack(fill="both", expand=True, padx=10, pady=10)

        # Configurar grid para os gráficos
        self.frame_graficos.grid_rowconfigure(0, weight=1)
        self.frame_graficos.grid_rowconfigure(1, weight=1)
        self.frame_graficos.grid_columnconfigure(0, weight=1)
        self.frame_graficos.grid_columnconfigure(1, weight=1)

        # Dividindo em 2x2 para exibir os gráficos
        self.frame_saldo = tk.Frame(self.frame_graficos, bg=self.bg_janela)
        self.frame_saldo.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.frame_linha = tk.Frame(self.frame_graficos, bg=self.bg_janela)
        self.frame_linha.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.frame_barras = tk.Frame(self.frame_graficos, bg=self.bg_janela)
        self.frame_barras.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.frame_pizza = tk.Frame(self.frame_graficos, bg=self.bg_janela)
        self.frame_pizza.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # Botão de "Relatório Financeiro"
        self.botao_relatorio = tk.Button(self, text="Relatório Financeiro", command=self.gerar_relatorio, font=("Arial", 12), bg=self.bg_cor, fg="white")
        self.botao_relatorio.pack(pady=10)

        # Atualizar o saldo ao iniciar
        self.atualizar_saldo()

        # Mostrar os gráficos
        self.plot_linha()
        self.plot_barras()
        self.plot_pizza()

    def conectar_bd(self):
        return sqlite3.connect('clientes.bd')

    def atualizar_saldo(self):
        conn = self.conectar_bd()
        cursor = conn.cursor()

        # Obter o saldo total
        cursor.execute("SELECT SUM(valor) FROM lancamento WHERE tipo = 'entrada'")
        entradas = cursor.fetchone()[0] or 0

        cursor.execute("SELECT SUM(valor) FROM lancamento WHERE tipo = 'saida'")
        saidas = cursor.fetchone()[0] or 0

        saldo_total = entradas - saidas

        self.saldo_label.config(text=f"Saldo Atual: R$ {saldo_total:.2f}")
        conn.close()

    def plot_barras(self):
        largura_tela = self.winfo_width()
        altura_tela = self.winfo_height()

        # Ajustando o gráfico com base no recuo de 20%
        largura_ajustada = largura_tela * 0.45
        altura_ajustada = altura_tela * 0.40

        conn = self.conectar_bd()
        cursor = conn.cursor()

        cursor.execute("SELECT data, tipo FROM lancamento")
        registros = cursor.fetchall()
        conn.close()

        # Processar dados
        df = pd.DataFrame(registros, columns=['data', 'tipo'])
        df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')
        df['mes_ano'] = df['data'].dt.strftime('%Y-%m')

        entradas = df[df['tipo'] == 'entrada'].groupby('mes_ano').size()
        saidas = df[df['tipo'] == 'saida'].groupby('mes_ano').size()

        meses = sorted(set(df['mes_ano']))
        entradas = [entradas.get(mes, 0) for mes in meses]
        saidas = [saidas.get(mes, 0) for mes in meses]

        fig, ax = plt.subplots(figsize=(largura_ajustada / 100, altura_ajustada / 100))  # Ajuste do gráfico
        largura_barra = 0.4
        posicoes_x = range(len(meses))

        ax.bar([x - largura_barra / 2 for x in posicoes_x], entradas, width=largura_barra, label='Entradas', color='#66b2b2')
        ax.bar([x + largura_barra / 2 for x in posicoes_x], saidas, width=largura_barra, label='Saídas', color='#ff6666')

        ax.set_xlabel('Mês/Ano', fontsize=10, color=self.text_cor)
        ax.set_ylabel('Número de Lançamentos', fontsize=10, color=self.text_cor)
        ax.set_title('Entradas X Saídas por Mês', fontsize=12, color=self.title_cor)
        ax.set_xticks(posicoes_x)
        ax.set_xticklabels(meses, rotation=45, fontsize=8, color=self.text_cor)
        ax.legend(fontsize=8)

        self._show_plot(fig, self.frame_barras)

    def plot_pizza(self):
        largura_tela = self.winfo_width()
        altura_tela = self.winfo_height()

        # Ajustando o gráfico com base no recuo de 20%
        largura_ajustada = largura_tela * 0.45
        altura_ajustada = altura_tela * 0.40

        conn = self.conectar_bd()
        cursor = conn.cursor()

        cursor.execute("SELECT nome, valor FROM lancamento")
        registros = cursor.fetchall()
        conn.close()

        df = pd.DataFrame(registros, columns=['nome', 'valor'])
        distribuicao = df.groupby('nome')['valor'].sum()

        cores_contrastes = ['#66b2b2', '#ff6666', '#1e2a47', '#ffcc99', '#8e44ad', '#f39c12']

        fig, ax = plt.subplots(figsize=(largura_ajustada / 100, altura_ajustada / 100))
        ax.pie(distribuicao, labels=distribuicao.index, autopct='%1.1f%%', colors=cores_contrastes[:len(distribuicao)])
        ax.set_title("Distribuição por Produtos", fontsize=12, color="#1e2a47")

        self._show_plot(fig, self.frame_pizza)

    def plot_linha(self):
        largura_tela = self.winfo_width()
        altura_tela = self.winfo_height()

        largura_ajustada = largura_tela * 0.45
        altura_ajustada = altura_tela * 0.40

        conn = self.conectar_bd()
        cursor = conn.cursor()

        cursor.execute("SELECT data, saldo FROM lancamento")
        registros = cursor.fetchall()
        conn.close()

        df = pd.DataFrame(registros, columns=['data', 'saldo'])
        df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')
        df.sort_values(by='data', inplace=True)

        datas = df['data'].dt.strftime('%Y-%m-%d').tolist()
        saldos = df['saldo'].tolist()

        datas = [datetime.strptime(data, "%Y-%m-%d") for data in datas]

        fig, ax = plt.subplots(figsize=(largura_ajustada / 100, altura_ajustada / 100))
        ax.plot(datas, saldos, marker='o', color='#66b2b2')

        ax.set_title("Evolução do Saldo", fontsize=12, color=self.title_cor)
        ax.xaxis.set_major_formatter(DateFormatter("%Y-%m"))
        ax.set_xticks(datas)
        ax.set_xticklabels([data.strftime("%Y-%m") for data in datas], rotation=45, fontsize=8, color=self.text_cor)

        self._show_plot(fig, self.frame_linha)

    def _show_plot(self, fig, frame):
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def gerar_relatorio(self):
        # Lógica para gerar o relatório financeiro
        messagebox.showinfo("Relatório", "Relatório financeiro gerado com sucesso!")

    def on_closing(self):
        self.destroy()
        self.quit()


# Iniciar o aplicativo
app = DashboardFinanceiro()
app.protocol("WM_DELETE_WINDOW", app.on_closing)
app.mainloop()
