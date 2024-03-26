from tabula.io import read_pdf
from pprint import pprint
import pandas as pd
from pandas import read_excel

# from tabulate import tabulate
import warnings

# Ignorar erros
warnings.filterwarnings("default")

# Lendo PDF como binario
pdf_file = open("72380.pdf", "rb")

# Lendo as tabnelas no PDF
tabelas = read_pdf(pdf_file, pages="all", silent=True)

# Lista das tabelas a serem extraídas pelo index
tabelas_desejadas = [
    "Descrição de Créditos e Descontos do Reclamante",
    "Descrição do Bruto Devido ao Reclamante",
    "Descrição de Débitos do Reclamado por Credor",
]

# Extrai as tabelas acima
for nome in tabelas_desejadas:
    for tabela in tabelas:
        if nome in tabela.columns:
            tabela.to_excel(f"{nome}.xlsx", index=False)
            break


# Ler e ajustar planilha de DE/PARA
dp = read_excel(r"C:\Users\vinic\Downloads\Projuris - teste\RPA - De Para.xlsx")

dp["DE"].loc[:] = dp["DE"].str.strip().str.upper()
dp["PARA"].loc[:] = dp["PARA"].str.strip().str.upper()

# Ler e ajustar as planilhas
holerite = read_excel(r"Descrição do Bruto Devido ao Reclamante.xlsx")
holerite["Descrição do Bruto Devido ao Reclamante"].loc[:] = (
    holerite["Descrição do Bruto Devido ao Reclamante"].str.strip().str.upper()
)

# Definir índices para cruzamento
dp.set_index("DE", inplace=True)
holerite.set_index("Descrição do Bruto Devido ao Reclamante", inplace=True)

# Juntar os DF como tabelas
# Left = O que não encontrar, repete as colunas originais e preenche o resto como NaN
df = holerite.join(dp, how="left")

# Preencher valores ausentes com 0
df.fillna(0, inplace=True)

# Agrupar pelo valor da coluna "PARA" e somar os valores agrupados
df_soma = df.groupby("PARA").sum()

print(df)
df_soma = df_soma.reset_index()  # Resetar o índice para converter o DataFrame em uma lista de dicionários
df_soma = df_soma.to_dict("records")
# df = df.to_dict("records")

print("FIM")
