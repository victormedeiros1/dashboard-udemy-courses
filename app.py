import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("Dashboard de Estatísticas - Cursos Udemy")

# Carregar os dados
df = pd.read_csv("udemy_courses.csv")

# Filtro de nível
levels = df["level"].unique().tolist()
selected_levels = st.multiselect("Filtrar por nível:", levels, default=levels)

# Aplicar filtro
df_filtered = df[df["level"].isin(selected_levels)]

# Seletor de layout
layout = st.radio("Escolha o layout de visualização:", ["Colunas", "Linha única"])

# 1. Top 10 cursos com mais inscritos
top_cursos = df_filtered.sort_values(by="num_subscribers", ascending=False).head(10)
fig1 = px.bar(top_cursos, x="course_title", y="num_subscribers", title="Top 10 Cursos com Mais Inscritos")

# 2. Preço médio por categoria
preco_medio = df_filtered[df_filtered['is_paid'] == True].groupby("subject")["price"].mean().reset_index()
fig2 = px.bar(preco_medio, x="subject", y="price", title="Preço Médio por Categoria (Cursos Pagos)")

# 3. Preço vs Número de Inscritos
fig3 = px.scatter(df_filtered[df_filtered['is_paid'] == True], x="price", y="num_subscribers",
                  size="num_reviews", color="subject",
                  title="Preço vs Inscritos (Cursos Pagos)")

# 4. Distribuição por nível (ainda com todos os dados, ou só filtrados?)
fig4 = px.pie(df_filtered, names="level", title="Distribuição de Cursos por Nível")

# 5. Duração do curso vs inscritos
fig5 = px.scatter(df_filtered, x="content_duration", y="num_subscribers",
                  color="subject",
                  title="Duração do Curso vs Número de Inscritos")

# 6. Cursos pagos vs gratuitos
pagos_vs_gratis = df_filtered['is_paid'].value_counts().reset_index()
pagos_vs_gratis.columns = ['Tipo', 'Quantidade']
pagos_vs_gratis['Tipo'] = pagos_vs_gratis['Tipo'].replace({True: 'Pago', False: 'Gratuito'})
fig6 = px.pie(pagos_vs_gratis, names='Tipo', values='Quantidade', title='Cursos Pagos vs Gratuitos')

# Lista de figuras
figures = [fig1, fig2, fig3, fig4, fig5, fig6]

# Exibição com base no layout escolhido
if layout == "Colunas":
    for i in range(0, len(figures), 2):
        cols = st.columns(2)
        cols[0].plotly_chart(figures[i], use_container_width=True)
        if i + 1 < len(figures):
            cols[1].plotly_chart(figures[i + 1], use_container_width=True)
else:
    for fig in figures:
        st.plotly_chart(fig, use_container_width=True)
