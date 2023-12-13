import streamlit as st
import pandas as pd
# import plotly as px
import numpy as np
import matplotlib.pyplot as plt

st.header(" *Dados de vendas de jogos dentro da plataforma PS4*")
st.write("""  Essa aplicação tem como intuito de analisar os dados de jogos do ps4. 
         Como a quantidade de vendas em unidades no periodo do ano que ele foi lançado dentro da plataforma.                            
            O csv tem 93,7 kbs de tamanho | 712 linhas | 9 colunas de (JOGO, ANO DE LANÇAMENTO, GÊNERO, EDITORA, VENDAS AMERICA DO NORTE, EUROPA, JAPÃO, RESTO DO MUNDO, GLOBAL)
         
         """)

# Lê o arquivo CSV
df = pd.read_csv('PS4GamesSales.csv', encoding='latin1')

# Exibe o DataFrame
st.dataframe(df)

st.write("Dados de filtragem")

# Ano de Lançamento
Year = st.sidebar.multiselect(
    key=1,
    label="Ano",
    options=df["Year"].unique()
)

# Gênero
Genre = st.sidebar.multiselect(
    key=2,
    label="Gênero",
    options=df["Genre"].unique()
)

# Editora
Publisher = st.sidebar.multiselect(
    key=3,
    label="Editora",
    options=df["Publisher"].unique()
)

# Região
selected_regions = st.sidebar.multiselect(
    key=4,
    label="Região",
    options=df.columns[4:]  # Ajuste de acordo com a posição das colunas de região no seu DataFrame
)

# Filtro no DataFrame
df_filtered = df.query("Year == @Year and Genre == @Genre and Publisher == @Publisher")

# Filtra por região se alguma região foi selecionada
if selected_regions:
    df_filtered = df_filtered[['Game','Year', 'Genre', 'Publisher'] + selected_regions]

# Exibe o DataFrame filtrado
st.dataframe(df_filtered)

st.markdown("***")

#------------------------------ Gráficos ----------------------------------------------


#Gráfico de barra de vendas por região 

st.write("Soma de vendas por região de 2013 a 2018")

fig3, ax3 = plt.subplots(figsize=(6, 6))

soma_america = df['NorthAmerica'].sum()
soma_europe = df['Europe'].sum()
soma_japan = df['Japan'].sum()
soma_rest = df['RestofWorld'].sum()

bars = plt.bar(['América do Norte', 'Europa', 'Japão', 'Resto do Mundo'], [soma_america, soma_europe, soma_japan, soma_rest])
plt.xlabel('Região')
plt.ylabel('Unidades vendidas em milhões')
plt.title('Soma de Vendas por Região')

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, yval, round(yval, 1), ha='center', va='bottom', fontsize=8)

# Mostrar o gráfico no Streamlit
st.pyplot(plt)

st.markdown("***")

#-----------------------------------------------------------------------------------------------

#gráfico de pizza de vendas por região em porcentagem

st.write("Vendas de jogos por regiões em porcentagem")

# Calcular as vendas totais por região
df['TotalSales'] = df[['NorthAmerica', 'Europe', 'Japan', 'RestofWorld']].sum(axis=1)

# Criar uma figura com tamanho personalizado
fig, ax = plt.subplots(figsize=(8, 8))

# Calcular as somas por região
soma_america = df['NorthAmerica'].sum()
soma_europe = df['Europe'].sum()
soma_japan = df['Japan'].sum()
soma_rest = df['RestofWorld'].sum()

# Criar o gráfico de pizza
plt.pie([soma_america, soma_europe, soma_japan, soma_rest], labels=['América do Norte', 'Europa', 'Japão', 'Resto do mundo'], autopct='%1.1f%%', startangle=90)

# Adicionar título
plt.title('Vendas de jogos por regiões')

# Mostrar o gráfico no Streamlit
st.pyplot(fig)

st.markdown("***")



#-----------------------------------------------------------------------------------------------

st.write("Gráfico de pizza de vendas de jogos global")

# Criar uma figura com tamanho personalizado
fig, ax = plt.subplots(figsize=(10, 10))

# Agrupar por jogo e calcular as vendas globais
vendas_por_jogo = df.groupby('Game')['Global'].sum().sort_values(ascending=False)

# Limitar o número de jogos para o exemplo (você pode ajustar conforme necessário)
top_n_jogos = 25 #Escolher quantidade de jogos para gráfico
vendas_por_jogo = vendas_por_jogo.head(top_n_jogos)

# Criar o gráfico de pizza
plt.pie(vendas_por_jogo, labels=vendas_por_jogo.index, autopct='%1.1f%%', startangle=90)

# Adicionar título
plt.title('Vendas Globais por Jogo (Top 25)')

# Mostrar o gráfico no Streamlit
st.pyplot(fig)

st.markdown("***")

#-----------------------------------------------------------------------------------------------

# Gráfico de barras de contagem de jogos por editora
st.write("Contagem de jogos por editora")

contagem_por_editora = df['Publisher'].value_counts()

# Selecionar as 25 maiores contagens
contagem_top25 = contagem_por_editora.head(50)

# Criar uma figura com tamanho personalizado
fig, ax = plt.subplots(figsize=(10, 6))

# Criar um gráfico de barras usando as 25 maiores contagens
bars = plt.bar(contagem_top25.index, contagem_top25)
plt.xlabel('Editoras')
plt.ylabel('Número de Jogos')
plt.title('Contagem de Jogos por Editora (Top 50)')

# Rotacionar os rótulos do eixo x
plt.xticks(rotation='vertical', fontsize=8)

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, yval, round(yval, 1), ha='center', va='bottom', fontsize=8)

# Mostrar o gráfico no Streamlit
st.pyplot(plt)


st.markdown("***")

#------------------------------------------------------------------------------------------------

# Válido contagem de jogos

st.write("Contagem de jogos por gênero")

contagem_por_genero = df['Genre'].value_counts()

fig2, ax2 = plt.subplots(figsize=(6, 6))

# Criar um gráfico de barras usando a contagem por gênero
bars1 = plt.bar(contagem_por_genero.index, contagem_por_genero)
plt.xlabel('Gênero')
plt.ylabel('Número de Jogos')
plt.title('Contagem de Jogos por Gênero')

# Rotacionar os rótulos do eixo x
plt.xticks(rotation='vertical')

for bar in bars1:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, yval, round(yval, 1), ha='center', va='bottom', fontsize=8)

# Mostrar o gráfico no Streamlit
st.pyplot(plt)

st.markdown("***")

# ----------------------------------Tela info---------------------------------------------------

st.write("""
    # *Tela de info*
""")

# Ano de Lançamento
Game = st.multiselect(
    label="Selecionar jogos",
    options=df["Game"].unique()
)


# Filtro no DataFrame
df_filtered = df

# Filtra por ano se algum ano foi selecionado
if Game:
    df_filtered = df_filtered[df_filtered["Game"].isin(Game)]

# Filtra por região se alguma região foi selecionada
if selected_regions:
    df_filtered = df_filtered['Game']

# Exibe o DataFrame filtrado
st.write("Dados selecionados:")
st.dataframe(df_filtered)
