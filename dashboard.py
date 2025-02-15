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
        self.geometry("800x600")  # Ajustando a janela para um tamanho maior

        # Definindo as cores principais com a paleta fornecida
        self.bg_cor = "#436778"  # Azul escuro
        self.highlight_bg = "#2c4c5c"  # Azul mais escuro para bordas
        self.btn_bg = "#abcad9"  # Azul claro para botões
        self.btn_fg = "black"  # Cor de texto dos botões
        self.bg_janela = "#f4f4f9"  # Cor de fundo suave (cinza claro)
        self.text_cor = "#333333"  # Cor do texto (cinza escuro)
        self.title_cor = "#1e2a47"  # Cor do título (tom escuro de azul)

        # Configurando a cor de fundo da janela principal
        self.config(bg=self.bg_janela)

        # Adicionar seção para saldo
        self.saldo_label = tk.Label(self, text="Saldo Atual: R$ 0.00", font=("Arial", 14), fg=self.text_cor, bg=self.bg_janela)
        self.saldo_label.pack(pady=10)

        # Botões para os gráficos
        self.plot_barras_button = tk.Button(self, text="Exibir Gráfico de Entradas e Saídas", command=self.plot_barras, bg=self.btn_bg, fg=self.btn_fg, font=("Arial", 12))
        self.plot_barras_button.pack(pady=10)

        self.plot_pizza_button = tk.Button(self, text="Exibir Gráfico de Produtos", command=self.plot_pizza, bg=self.btn_bg, fg=self.btn_fg, font=("Arial", 12))
        self.plot_pizza_button.pack(pady=10)

        self.plot_linha_button = tk.Button(self, text="Exibir Gráfico Evolução de Saldo", command=self.plot_linha, bg=self.btn_bg, fg=self.btn_fg, font=("Arial", 12))
        self.plot_linha_button.pack(pady=10)

        self.export_button = tk.Button(self, text="Exportar Relatório", command=self.export_relatorio, bg=self.btn_bg, fg=self.btn_fg, font=("Arial", 12))
        self.export_button.pack(pady=10)

        # Armazenar os gráficos para evitar sobreposição
        self.current_canvas = None

        # Atualizar o saldo ao iniciar
        self.atualizar_saldo()

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
        largura_ajustada = largura_tela * 0.80
        altura_ajustada = altura_tela * 0.80

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

        ax.set_xlabel('Mês/Ano', fontsize=10, color=self.text_cor)  # Ajustando o tamanho da fonte
        ax.set_ylabel('Número de Lançamentos', fontsize=10, color=self.text_cor)  # Ajustando o tamanho da fonte
        ax.set_title('Número de Entradas e Saídas por Mês', fontsize=12, color=self.title_cor)  # Ajustando o título
        ax.set_xticks(posicoes_x)
        ax.set_xticklabels(meses, rotation=45, fontsize=8, color=self.text_cor)  # Ajustando o tamanho da fonte das legendas
        ax.legend(fontsize=8)  # Ajustando o tamanho da fonte da legenda

        self._show_plot(fig)

    def plot_pizza(self):
        largura_tela = self.winfo_width()
        altura_tela = self.winfo_height()

        # Ajustando o gráfico com base no recuo de 20%
        largura_ajustada = largura_tela * 0.80
        altura_ajustada = altura_tela * 0.80

        conn = self.conectar_bd()
        cursor = conn.cursor()

        cursor.execute("SELECT nome, valor FROM lancamento")
        registros = cursor.fetchall()
        conn.close()

        df = pd.DataFrame(registros, columns=['nome', 'valor'])
        distribuicao = df.groupby('nome')['valor'].sum()

        # Cores mais contrastantes
        cores_contrastes = ['#66b2b2', '#ff6666', '#1e2a47', '#ffcc99', '#8e44ad', '#f39c12']

        fig, ax = plt.subplots(figsize=(largura_ajustada / 100, altura_ajustada / 100))  # Ajuste do gráfico
        ax.pie(distribuicao, labels=distribuicao.index, autopct='%1.1f%%', colors=cores_contrastes[:len(distribuicao)])
        ax.set_title("Distribuição de Produtos Lançados", fontsize=12, color="#1e2a47")  # Ajustando o título

        self._show_plot(fig)

    def plot_linha(self):
        largura_tela = self.winfo_width()
        altura_tela = self.winfo_height()

        # Ajustando o gráfico com base no recuo de 20%
        largura_ajustada = largura_tela * 0.80
        altura_ajustada = altura_tela * 0.80

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

        fig, ax = plt.subplots(figsize=(largura_ajustada / 100, altura_ajustada / 100))  # Ajuste do gráfico
        ax.plot(datas, saldos, marker='o', color='#66b2b2')

        ax.set_title("Evolução do Saldo", fontsize=12, color=self.title_cor)  # Ajustando o título
        ax.xaxis.set_major_formatter(DateFormatter("%Y-%m"))
        ax.set_xticks(datas)
        ax.set_xticklabels([data.strftime("%Y-%m") for data in datas], rotation=45, fontsize=8, color=self.text_cor)  # Ajustando o tamanho da fonte das legendas

        self._show_plot(fig)

    def export_relatorio(self):
        conn = self.conectar_bd()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM lancamento")
        registros = cursor.fetchall()
        conn.close()

        df = pd.DataFrame(registros, columns=['Código', 'Data', 'Valor', 'Tipo', 'Nome', 'Saldo'])
        df.to_excel("relatorio_financeiro.xlsx", index=False)
        messagebox.showinfo("Exportação", "Relatório exportado com sucesso!")

    def _show_plot(self, fig):
        # Remover o gráfico atual, se existir
        if self.current_canvas:
            self.current_canvas.get_tk_widget().pack_forget()

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=20)
        self.current_canvas = canvas

    def on_closing(self):
        self.destroy()
        self.quit()


# Iniciar o aplicativo
app = DashboardFinanceiro()
app.protocol("WM_DELETE_WINDOW", app.on_closing)
app.mainloop()