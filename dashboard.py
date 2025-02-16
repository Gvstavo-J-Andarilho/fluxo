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
        super().__init__() #iniciar janela
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

        '''# Adicionar seção para saldo
        self.saldo_label = tk.Label(self, text="Saldo Atual: R$ ", font=("Arial", 18), fg=self.bg_janela, bg=self.highlight_bg)
        self.saldo_label.pack(pady=5) #distancia do que tá escrito em cima da borda superior'''

        # Frame/janela principal onde os gráficos serão dispostos
        self.frame_graficos = tk.Frame(self, bg=self.highlight_bg)
        self.frame_graficos.pack(fill="both", expand=True, padx=10, pady=10)

        # Configurar grid para os gráficos
        self.frame_graficos.grid_rowconfigure(0, weight=1)
        self.frame_graficos.grid_rowconfigure(1, weight=1)
        self.frame_graficos.grid_columnconfigure(0, weight=1)
        self.frame_graficos.grid_columnconfigure(1, weight=1)

        # Dividindo os frames/quadros em 2x2 para exibir os gráficos
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
        '''self.atualizar_saldo()'''
        # Mostrar variação percentual no primeiro quadrado superior esquerdo
        self.plot_variacao_percentual()

        # Mostrar os gráficos
        self.plot_linha()
        self.plot_barras()
        self.plot_pizza()

    #Puxa os dados do banco de dados de lançamento do 'fluxo de caixa'
    def conectar_bd(self):
        return sqlite3.connect('clientes.bd')

    #saldo atualizado do banco de dados
    def atualizar_saldo(self):
        conn = self.conectar_bd()
        cursor = conn.cursor()

        # Obter o saldo total diretamente do banco de dados
        cursor.execute("SELECT SUM(valor) FROM lancamento WHERE tipo = 'entrada'")
        entradas = cursor.fetchone()[0] or 0

        cursor.execute("SELECT SUM(valor) FROM lancamento WHERE tipo = 'saida'")
        saidas = cursor.fetchone()[0] or 0

        saldo_total = entradas - saidas

        self.saldo_label.config(text=f"Saldo Atual: R$ {saldo_total:.2f}")
        conn.close()

    def plot_variacao_percentual(self):
        largura_tela = self.winfo_width()
        altura_tela = self.winfo_height()

        # Ajustando o gráfico com base no recuo de 20%
        largura_ajustada = largura_tela * 0.35
        altura_ajustada = altura_tela * 0.30

        conn = self.conectar_bd()
        cursor = conn.cursor()

        cursor.execute("SELECT data, saldo FROM lancamento")
        registros = cursor.fetchall()
        conn.close()

        # Processar dados
        df = pd.DataFrame(registros, columns=['data', 'saldo'])
        df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')
        df.sort_values(by='data', inplace=True)
        df['mes_ano'] = df['data'].dt.to_period('M')
        df = df.groupby('mes_ano')['saldo'].last().reset_index()  # Último saldo de cada mês
        df['variacao'] = df['saldo'].pct_change() * 100  # Calcula a variação percentual
        df.dropna(inplace=True)  # Remove o primeiro valor que será NaN

        datas = df['mes_ano'].dt.strftime('%Y-%m').tolist()
        variacoes = df['variacao'].tolist()
        datas = [datetime.strptime(data, "%Y-%m") for data in datas]

        fig, ax = plt.subplots(figsize=(largura_ajustada / 100, altura_ajustada / 100))

        # Plotando a linha de variação percentual
        ax.plot(datas, variacoes, marker='o', linestyle='-', color='#1e2a47', label='Variação %')
        ax.axhline(0, color='gray', linestyle='--', linewidth=0.5)  # Linha de referência no zero

        ax.set_title("Variação % do Saldo", fontsize=12, color=self.title_cor)
        ax.set_ylabel("Variação %", fontsize=10, color=self.text_cor)
        ax.xaxis.set_major_formatter(DateFormatter("%Y-%m"))
        ax.set_xticks(datas)
        ax.set_xticklabels([data.strftime("%Y-%m") for data in datas], rotation=0, fontsize=8, color=self.text_cor)
        ax.legend(fontsize=8)

        # Remover gráficos anteriores para evitar sobreposição
        for widget in self.frame_saldo.winfo_children():
            widget.destroy()

        # Exibir o saldo atualizado acima do gráfico de variação percentual
        saldo_atual = df['saldo'].iloc[-1]  # Pega o último saldo registrado
        saldo_label = tk.Label(self.frame_saldo, text=f"Saldo Atual: R$ {saldo_atual:.2f}",
                               font=("Arial", 14), fg=self.title_cor, bg=self.bg_janela)
        saldo_label.pack(pady=5)

        # Mostrar o gráfico logo abaixo do saldo
        self._show_plot(fig, self.frame_saldo)

    def plot_barras(self):
        largura_tela = self.winfo_width()
        altura_tela = self.winfo_height()

        # Ajustando o gráfico com base no recuo de 20%
        largura_ajustada = largura_tela * 0.25
        altura_ajustada = altura_tela * 0.20

        conn = self.conectar_bd() #conecta ao Banco de dados do 'Fluxo de caixa' (FC)
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
        ax.set_xticklabels(meses, rotation=0, fontsize=8, color=self.text_cor)
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

        largura_ajustada = largura_tela * 0.35
        altura_ajustada = altura_tela * 0.30

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

        # Preenche a área positiva (saldo >= 0) com cor verde
        ax.fill_between(datas, saldos, where=[saldo >= 0 for saldo in saldos], color='#66b2b2', alpha=0.6,
                        label="Saldo Positivo")

        # Preenche a área negativa (saldo < 0) com cor vermelha
        ax.fill_between(datas, saldos, where=[saldo < 0 for saldo in saldos], color='#ff6666', alpha=0.6,
                        label="Saldo Negativo")

        ax.set_title("Evolução do Saldo", fontsize=12, color=self.title_cor)
        ax.xaxis.set_major_formatter(DateFormatter("%Y-%m"))
        ax.set_xticks(datas)
        ax.set_xticklabels([data.strftime("%Y-%m") for data in datas], rotation=0, fontsize=8, color=self.text_cor)
        ax.legend(fontsize=8) #tamanho da fonte de legenda do gráfico

        self._show_plot(fig, self.frame_linha)


    def _show_plot(self, fig, frame):
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def gerar_relatorio(self):
        try:
            conn = self.conectar_bd()
            cursor = conn.cursor()

            # 1. Obter todos os lançamentos do banco de dados, incluindo o código
            cursor.execute("SELECT codigo, data, valor, tipo, nome, saldo FROM lancamento ORDER BY data")
            registros = cursor.fetchall()
            conn.close()

            # 2. Criar DataFrame com os lançamentos, incluindo o código
            df = pd.DataFrame(registros, columns=['Código', 'Data', 'Valor', 'Tipo', 'Nome', 'Saldo'])

            # Converter e formatar a data para dd/mm/aaaa (sem horários)
            df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y').dt.strftime('%d/%m/%Y')

            # Ordenar pelo código para manter a sequência do banco de dados
            df.sort_values(by='Código', inplace=True)

            # 3. Calcular Resumo Geral
            saldo_inicial = df['Saldo'].iloc[0] if not df.empty else 0
            saldo_final = df['Saldo'].iloc[-1] if not df.empty else 0
            variacao_percentual = ((saldo_final - saldo_inicial) / saldo_inicial) * 100 if saldo_inicial != 0 else 0
            entradas_totais = df[df['Tipo'] == 'entrada']['Valor'].sum()
            saidas_totais = df[df['Tipo'] == 'saida']['Valor'].sum()

            resumo = {
                'Saldo Inicial (R$)': [saldo_inicial],
                'Saldo Final (R$)': [saldo_final],
                'Variação Percentual (%)': [variacao_percentual],
                'Total de Entradas (+R$)': [entradas_totais],
                'Total de Saídas (-R$)': [saidas_totais]
            }
            df_resumo = pd.DataFrame(resumo)

            # 4. Resumo Mensal
            df['Mes_Ano'] = pd.to_datetime(df['Data'], format='%d/%m/%Y').dt.to_period('M')
            resumo_mensal = df.groupby(['Mes_Ano', 'Tipo'])['Valor'].sum().unstack().fillna(0)
            resumo_mensal['Saldo Mensal'] = resumo_mensal.get('entrada', 0) - resumo_mensal.get('saida', 0)
            resumo_mensal.reset_index(inplace=True)

            # Remover a última coluna 'Mes_Ano' da DataFrame
            df.drop(columns=['Mes_Ano'], inplace=True)

            # 5. Exportar para Excel (.xlsx)
            nome_arquivo = "relatorio_financeiro.xlsx"
            with pd.ExcelWriter(nome_arquivo, engine='openpyxl') as writer:
                df_resumo.to_excel(writer, sheet_name='Resumo Geral', index=False)
                df.to_excel(writer, sheet_name='Detalhes dos Lançamentos', index=False)
                resumo_mensal.to_excel(writer, sheet_name='Resumo Mensal', index=False)

            messagebox.showinfo("Relatório", f"Relatório financeiro gerado com sucesso!\nSalvo como: {nome_arquivo}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar o relatório: {e}")

    def on_closing(self):
        self.destroy()
        self.quit()


# Iniciar o aplicativo
app = DashboardFinanceiro()
app.protocol("WM_DELETE_WINDOW", app.on_closing)
app.mainloop()
